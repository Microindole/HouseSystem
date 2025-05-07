import json

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, abort, flash # 导入 flash
from sqlalchemy import or_, and_ 
from datetime import datetime, timedelta
from flask_wtf import FlaskForm

# 导入所需模型
from models import HouseInfoModel, HouseStatusModel, LandlordModel, db, PrivateChannelModel, LoginModel, MessageModel, ComplaintModel, TenantModel # 加入ComplaintModel, TenantModel
from decorators import login_required, admin_required 


feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')

class CSRFOnlyForm(FlaskForm):
    pass

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

    if request.method == 'POST':
        sender = session['username']
        receiver = request.form.get('receiver', '').strip()
        content = request.form.get('content', '').strip()
        complaint_type = request.form.get('type', '投诉') # 获取信息类型
        # house_id = request.form.get('house_id') # 获取 house_id

        if content:
            # 如果是投诉且选择了房东作为被投诉人，并且选择了房源
            # 确保 house_id 只有在 complaint_type 为 '投诉' 且 receiver 是房东时才可能被使用
            # 实际保存时，ComplaintModel 可能没有 house_id 字段，需要确认
            # 如果 ComplaintModel 有 house_id 字段，并且您想保存它：
            # selected_house_id = request.form.get('house_id') if complaint_type == '投诉' else None

            complaint_to_save = ComplaintModel(
                sender=sender,
                # 只有当类型是“投诉”时，才真正考虑 receiver，否则反馈通常没有明确的被投诉人
                receiver=receiver if complaint_type == '投诉' and receiver else None,
                content=content,
                time=datetime.utcnow(), # 最好使用 UTC 时间存储
                type=complaint_type
                # 如果 ComplaintModel 有 house_id 并且您想保存:
                # house_id=selected_house_id if selected_house_id else None
            )
            db.session.add(complaint_to_save)
            db.session.commit()
            flash(f'{complaint_type}已提交！', 'success')
            return redirect(url_for('feedback.my_complaints')) # 跳转到我的投诉记录页面
        else:
            flash('内容不能为空！', 'danger')

    # ... (existing GET request rendering logic) ...
    landlord_objs = LandlordModel.query.all()
    tenant_objs = TenantModel.query.all()
    user_list = []
    for l in landlord_objs:
        user_list.append({'username': l.landlord_name, 'type': '房东'})
    for t in tenant_objs:
        user_list.append({'username': t.tenant_name, 'type': '租客'})

    my_houses = [] # 如果当前用户是房东，其名下的房源
    user_type = session.get('user_type')
    current_username = session.get('username')

    if user_type == 2:
        my_houses_query = HouseInfoModel.query.join(
            HouseStatusModel, HouseInfoModel.house_id == HouseStatusModel.house_id
        ).filter(HouseStatusModel.landlord_name == current_username).all()
        my_houses = [{'house_id': h.house_id, 'house_name': h.house_name} for h in my_houses_query]

    houses_for_template = []


    return render_template(
        'feedback/complaint.html',
        user_list=user_list,
        houses=houses_for_template,
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

@feedback_bp.route('/manage_complaints')
@login_required # 或者 @admin_required 如果只有管理员能处理
def manage_complaints():
    username = session.get('username')
    user_type = session.get('user_type')

    query = ComplaintModel.query.order_by(ComplaintModel.last_updated_time.desc())

    if user_type != 0: # 非管理员
        query = query.filter(ComplaintModel.receiver == username)
    
    complaints_raw = query.all()
    
    complaints_list_for_template = []
    for complaint_obj in complaints_raw:
        complaint_dict = {
            'complaint_id': complaint_obj.complaint_id,
            'sender': complaint_obj.sender,
            'receiver': complaint_obj.receiver,
            'content': complaint_obj.content,
            'time': complaint_obj.time.strftime('%Y-%m-%d %H:%M:%S') if complaint_obj.time else None,
            'type': complaint_obj.type,
            'status': complaint_obj.status,
            'handler_username': complaint_obj.handler_username,
            'last_updated_time': complaint_obj.last_updated_time.strftime('%Y-%m-%d %H:%M:%S') if complaint_obj.last_updated_time else None,
            'update_seen_by_sender': complaint_obj.update_seen_by_sender
        }
        complaints_list_for_template.append(complaint_dict)
    
    csrf_form = CSRFOnlyForm() # Create an instance of the CSRF form

    return render_template(
        'feedback/manage_complaints.html',
        complaints_list=complaints_list_for_template,
        form=csrf_form # Pass the form to the template
    )

@feedback_bp.route('/update_complaint_status/<int:complaint_id>', methods=['POST'])
@login_required # 或者 @admin_required
def update_complaint_status(complaint_id):
    complaint = ComplaintModel.query.get_or_404(complaint_id)
    username = session.get('username')
    user_type = session.get('user_type')

    if user_type != 0 and complaint.receiver != username:
        flash('您没有权限修改此投诉的状态。', 'danger')
        return redirect(url_for('feedback.manage_complaints'))

    new_status = request.form.get('status')

    if new_status not in ['待处理', '处理中', '已解决', '已关闭']:
        flash('无效的状态。', 'danger')
        return redirect(url_for('feedback.manage_complaints'))

    # 只有当状态真正发生改变时，才标记为需要通知发送者
    if complaint.status != new_status:
        complaint.status = new_status
        complaint.handler_username = username
        complaint.update_seen_by_sender = False # 标记为发送者未查看此更新
        # last_updated_time 会自动更新

        try:
            db.session.commit()
            flash(f'投诉 #{complaint_id} 状态已更新为 "{new_status}"。', 'success')
            # 此处可以添加主动通知发送者的逻辑 (邮件、系统消息等)
        except Exception as e:
            db.session.rollback()
            flash(f'更新投诉状态失败: {e}', 'danger')
    else:
        flash(f'投诉 #{complaint_id} 状态未发生变化。', 'info')
        
    return redirect(url_for('feedback.manage_complaints'))

@feedback_bp.route('/my_complaints')
@login_required
def my_complaints():
    current_username = session['username']
    my_complaints_list = ComplaintModel.query.filter_by(sender=current_username)\
        .order_by(ComplaintModel.last_updated_time.desc()).all() # 按最后更新时间排序更好

    # 将当前用户发送的、状态已更新且用户尚未查看的投诉标记为已查看
    # 只标记那些状态不是“待处理”的，因为“待处理”是初始状态，不需要特别“查看更新”
    ComplaintModel.query.filter(
        ComplaintModel.sender == current_username,
        ComplaintModel.update_seen_by_sender == False,
        ComplaintModel.status != '待处理' # 确保是状态被处理过的
    ).update({'update_seen_by_sender': True})
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # 可以记录错误，但不应阻止页面加载
        print(f"Error updating complaint seen status: {e}")

    return render_template('feedback/my_complaints.html', my_complaints_list=my_complaints_list)

