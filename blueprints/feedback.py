import json

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, abort, flash # 导入 flash
from sqlalchemy import or_
from datetime import datetime, timedelta

# 导入所需模型
from models import HouseInfoModel, HouseStatusModel, LandlordModel, db, PrivateChannelModel, LoginModel, MessageModel, ComplaintModel, TenantModel # 加入ComplaintModel, TenantModel
from decorators import login_required


feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')

@feedback_bp.route('/start_chat/<int:house_id>')
@login_required
def start_or_get_channel(house_id):
    # 1. 检查用户是否为租客
    if session.get('user_type') != 1:
        flash('只有租客才能发起与房东的对话。', 'warning')
        return redirect(url_for('house.house_detail', house_id=house_id))

    tenant_username = session.get('username')

    # 2. 查找房源状态以获取房东用户名
    house_status = HouseStatusModel.query.filter_by(house_id=house_id).first()
    if not house_status:
        abort(404, description="找不到该房源的状态信息。")

    landlord_username = house_status.landlord_name

    # 3. 查找或创建私信频道
    channel = PrivateChannelModel.query.filter_by(
        tenant_username=tenant_username,
        landlord_username=landlord_username,
        house_id=house_id
    ).first()

    if not channel:
        # 确保房东用户存在
        landlord_user = LoginModel.query.get(landlord_username)
        if not landlord_user:
             abort(400, description="房东用户不存在。")

        # 创建新频道
        channel = PrivateChannelModel(
            tenant_username=tenant_username,
            landlord_username=landlord_username,
            house_id=house_id
        )
        db.session.add(channel)
        try:
            db.session.commit()
            flash('已为您和房东建立新的沟通频道。', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"Error creating channel: {e}")
            flash('创建沟通频道失败，请稍后再试。', 'danger')
            return redirect(url_for('house.house_detail', house_id=house_id))

    # 统一跳转到 chat 路由
    return redirect(url_for('feedback.chat', channel_id=channel.channel_id))

# --- 新增发送消息的路由 ---
@feedback_bp.route('/send_message/<int:channel_id>', methods=['POST'])
@login_required
def send_message(channel_id):
    channel = PrivateChannelModel.query.get_or_404(channel_id)
    sender_username = session.get('username')
    content = request.form.get('content')

    # 权限检查：确保发送者是频道的一方
    if sender_username not in [channel.tenant_username, channel.landlord_username]:
        return jsonify({'success': False, 'error': '无权在此频道发送消息'}), 403

    if not content:
        return jsonify({'success': False, 'error': '消息内容不能为空'}), 400

    # 确定接收者
    receiver_username = channel.landlord_username if sender_username == channel.tenant_username else channel.tenant_username

    try:
        new_message = MessageModel(
            channel_id=channel_id,
            sender_username=sender_username,
            receiver_username=receiver_username,
            content=content,
            timestamp=datetime.utcnow() + timedelta(hours=8),  # 设置为北京时间
            # is_read 默认为 False
        )
        db.session.add(new_message)
        db.session.commit()

        # 返回成功响应和新消息的数据 (JS 可能需要)
        message_data = {
            'message_id': new_message.message_id,
            'channel_id': new_message.channel_id,
            'sender_username': new_message.sender_username,
            'content': new_message.content,
            'timestamp': new_message.timestamp.isoformat() + 'Z' # 返回 ISO 格式 UTC 时间
        }
        return jsonify({'success': True, 'message': message_data})

    except Exception as e:
        db.session.rollback()
        print(f"Error sending message: {e}")
        return jsonify({'success': False, 'error': '发送消息时发生内部错误'}), 500


@feedback_bp.route('/chat/<int:channel_id>')
@login_required
def chat(channel_id):
    username = session['username']

    channels = PrivateChannelModel.query.filter(
        (PrivateChannelModel.tenant_username == username) | 
        (PrivateChannelModel.landlord_username == username)
    ).all()

    channel_list = []
    for ch in channels:
        last_msg = MessageModel.query.filter_by(channel_id=ch.channel_id)\
            .order_by(MessageModel.timestamp.desc()).first()
        # 统计未读消息数（接收者是当前用户且未读）
        unread_count = MessageModel.query.filter_by(
            channel_id=ch.channel_id,
            receiver_username=username,
            is_read=False
        ).count()
        channel_list.append({
            'channel': ch,
            'last_message': last_msg,
            'unread_count': unread_count
        })

    current_channel = PrivateChannelModel.query.get_or_404(channel_id)
    house = HouseInfoModel.query.get(current_channel.house_id)
    messages = MessageModel.query.filter_by(channel_id=channel_id).order_by(MessageModel.timestamp.asc()).all()

    return render_template(
        'feedback/message.html',
        channels=channel_list,
        channel=current_channel,
        messages=messages,
        house=house
    )

@feedback_bp.route('/messages')
@login_required
def messages():
    username = session['username']
    # 查询所有与当前用户相关的频道
    channels = PrivateChannelModel.query.filter(
        (PrivateChannelModel.tenant_username == username) | 
        (PrivateChannelModel.landlord_username == username)
    ).all()

    # 构建频道列表及其最后一条消息
    channel_list = []
    for ch in channels:
        last_msg = MessageModel.query.filter_by(channel_id=ch.channel_id)\
            .order_by(MessageModel.timestamp.desc()).first()
        # 统计未读消息数（接收者是当前用户且未读）
        unread_count = MessageModel.query.filter_by(
            channel_id=ch.channel_id,
            receiver_username=username,
            is_read=False
        ).count()
        channel_list.append({
            'channel': ch,
            'last_message': last_msg,
            'unread_count': unread_count
        })

    # 不传 channel，不传 messages
    return render_template(
        'feedback/message.html',
        channels=channel_list,
        channel=None,
        messages=[]
    )

@feedback_bp.route('/set_read/<int:channel_id>', methods=['POST'])
@login_required
def set_read(channel_id):
    username = session['username']
    # 只将自己为接收者的消息设为已读
    MessageModel.query.filter_by(
        channel_id=channel_id,
        receiver_username=username,
        is_read=False
    ).update({'is_read': True})
    db.session.commit()
    return jsonify({'success': True})

@feedback_bp.route('/complaint', methods=['GET', 'POST'])
@login_required
def complaint():
    landlord_objs = LandlordModel.query.all()
    tenant_objs = TenantModel.query.all()
    user_list = []
    for l in landlord_objs:
        user_list.append({'username': l.landlord_name, 'type': '房东'})
    for t in tenant_objs:
        user_list.append({'username': t.tenant_name, 'type': '租客'})

    houses = []
    my_houses = []
    user_type = session.get('user_type')
    username = session.get('username')
    # 如果当前用户是房东，查找其房源
    if user_type == 2:
        my_houses = HouseInfoModel.query.join(HouseStatusModel, HouseInfoModel.house_id == HouseStatusModel.house_id)\
            .filter(HouseStatusModel.landlord_name == username).all()

    if request.method == 'POST':
        sender = session['username']
        receiver = request.form.get('receiver', '').strip()
        content = request.form.get('content', '').strip()
        house_id = request.form.get('house_id') or None

        # 判断被投诉人是否为房东，若是则获取其房源
        if receiver and any(u['username'] == receiver and u['type'] == '房东' for u in user_list):
            houses = HouseInfoModel.query.filter_by(landlord_name=receiver).all()
        else:
            houses = []

        # 提交表单时保存投诉
        if content:
            complaint = ComplaintModel(
                sender=sender,
                receiver=receiver if receiver else None,
                content=content,
                time=datetime.utcnow(),
                type='投诉'
            )
            db.session.add(complaint)
            db.session.commit()
            flash('投诉已提交！', 'success')
            return redirect(url_for('feedback.complaint'))

    return render_template(
        'feedback/complaint.html',
        user_list=user_list,
        houses=houses,
        my_houses=my_houses,
        user_type=user_type
    )


@feedback_bp.route('/get_houses_by_landlord')
@login_required
def get_houses_by_landlord():
    landlord_name = request.args.get('landlord_name', '').strip()
    # 先查 HouseStatusModel 拿到该房东的所有 house_id
    house_statuses = HouseStatusModel.query.filter_by(landlord_name=landlord_name).all()
    house_ids = [hs.house_id for hs in house_statuses]
    # 再查 HouseInfoModel 拿房源信息
    houses = HouseInfoModel.query.filter(HouseInfoModel.house_id.in_(house_ids)).all()
    house_list = [{'house_id': h.house_id, 'house_name': h.house_name} for h in houses]
    return jsonify({'houses': house_list})

