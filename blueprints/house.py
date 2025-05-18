import json
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, abort, flash, current_app
from sqlalchemy import or_
from datetime import datetime
from models import (HouseInfoModel, HouseStatusModel, CommentModel, NewsModel, 
                   TenantModel, LandlordModel, AppointmentModel, RepairRequestModel, db)
from decorators import login_required

house_bp = Blueprint('house', __name__)

# 允许的图片扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

with open('static/json/cities.json', 'r', encoding='utf-8') as f:
    cities_data = json.load(f)

@house_bp.route('', methods=['GET'])
def house_list():
    """房源列表页面 - 显示已上架的房源"""
    try:
        # 获取筛选条件
        region = request.args.get('region', '').strip()
        city = request.args.get('city', '').strip()
        keyword = request.args.get('keyword', '').strip()
        rooms = request.args.get('rooms', '').strip()
        address = request.args.get('address', '').strip()
        min_price = request.args.get('min_price', None, type=float)
        max_price = request.args.get('max_price', None, type=float)

        # 记录筛选条件
        selected_region = region or ''
        selected_city = city or ''

        # 基础查询 - 只显示上架状态(status=0)的房源，并连接房源状态表
        query = db.session.query(HouseInfoModel).join(
            HouseStatusModel, 
            HouseInfoModel.house_id == HouseStatusModel.house_id
        ).filter(HouseStatusModel.status == 0)

        # 应用筛选条件
        if address:
            query = query.filter(
                or_(
                    HouseInfoModel.addr.like(f"%{address}%"),
                    HouseInfoModel.region.like(f"%{address}%")
                )
            )

        if selected_region:
            query = query.filter(HouseInfoModel.region.like(f"%{selected_region}%"))

        if selected_city:
            query = query.filter(HouseInfoModel.region.like(f"%{selected_city}%"))

        if keyword:
            query = query.filter(
                or_(
                    HouseInfoModel.house_name.like(f"%{keyword}%"),
                    HouseInfoModel.addr.like(f"%{keyword}%"),
                    HouseInfoModel.highlight.like(f"%{keyword}%")
                )
            )

        if rooms == '4室及以上':
            query = query.filter(
                or_(
                    HouseInfoModel.rooms.like("4室%"),
                    HouseInfoModel.rooms.like("5室%"),
                    HouseInfoModel.rooms.like("6室%"),
                    HouseInfoModel.rooms.like("7室%"),
                    HouseInfoModel.rooms.like("8室%"),
                    HouseInfoModel.rooms.like("9室%"),
                    HouseInfoModel.rooms.like("10室%"),
                )
            )
        elif rooms:
            query = query.filter(HouseInfoModel.rooms.like(f"%{rooms}%"))

        if min_price is not None:
            query = query.filter(HouseInfoModel.price >= min_price)

        if max_price is not None:
            query = query.filter(HouseInfoModel.price <= max_price)

        # 按最新更新时间排序
        query = query.order_by(HouseStatusModel.update_time.desc())

        # 分页处理
        page = request.args.get('page', 1, type=int)
        per_page = 9
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        houses = pagination.items

        # 获取新闻列表
        news_list = NewsModel.query.order_by(NewsModel.time.desc()).limit(10).all()

        # 调试日志
        current_app.logger.info(f"房源列表查询: 找到{len(houses)}套房源, 第{page}页, 共{pagination.pages}页")

        # 构建筛选条件字典
        filters = {
            'region': selected_region,
            'city': selected_city,
            'keyword': keyword or '',
            'rooms': rooms or '',
            'min_price': min_price,
            'max_price': max_price,
            'address': address or ''
        }

        return render_template(
            'house/house_list.html',
            houses=houses,
            news_list=news_list,
            cities_data=cities_data,
            selected_region=selected_region,
            selected_city=selected_city,
            pagination=pagination,
            filters=filters
        )

    except Exception as e:
        current_app.logger.error(f"房源列表页面错误: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # 发生错误时返回空列表
        return render_template(
            'house/house_list.html',
            houses=[],
            news_list=[],
            cities_data=cities_data,
            selected_region='',
            selected_city='',
            pagination=None,
            filters={
                'region': '',
                'city': '',
                'keyword': '',
                'rooms': '',
                'min_price': None,
                'max_price': None,
                'address': ''
            }
        )  
@house_bp.route('/<int:house_id>', methods=['GET'])
def house_detail(house_id):
    # 查找房源信息
    house = HouseInfoModel.query.get(house_id)
    if not house:
        flash('房源不存在', 'error')
        abort(404)

    # 查找房源状态
    status = HouseStatusModel.query.filter_by(house_id=house_id).first()
    if not status:
        flash('房源状态信息不存在', 'error')
        abort(404)
    
    # 检查房源是否对当前用户可见
    user_type = session.get('user_type')
    username = session.get('username')
    
    # 如果不是房东本人，只能查看已上架的房源
    if user_type != 2 or (user_type == 2 and status.landlord_name != username):
        if status.status != 0:  # 不是已上架状态
            flash('该房源暂不可查看', 'error')
            return redirect(url_for('house.house_list'))
    
    # 获取当前用户信息
    user = None
    if user_type == 1:  # 租客
        user = TenantModel.query.filter_by(tenant_name=username).first()
    elif user_type == 2:  # 房东
        user = LandlordModel.query.filter_by(landlord_name=username).first()
    
    # 分页处理评论
    page = request.args.get('page', 1, type=int)
    per_page = 10

    pagination = CommentModel.query.filter_by(
        house_id=house_id
    ).order_by(
        CommentModel.time.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    comments_on_page = pagination.items

    # 处理评论的 @ 信息
    enriched_comments = []
    for comment in comments_on_page:
        comment_data = {
            'comment_id': comment.comment_id,
            'username': comment.username,
            'type': comment.type,
            'desc': comment.desc,
            'time': comment.time,
            'at': comment.at,
            'at_username': None,
            'at_desc': None
        }
        if comment.at:
            at_comment = CommentModel.query.filter_by(comment_id=comment.at).first()
            if at_comment:
                comment_data['at_username'] = at_comment.username
                comment_data['at_desc'] = at_comment.desc
        enriched_comments.append(comment_data)

    # 调试信息（开发时使用）
    current_app.logger.info(f"房源详情: house_id={house_id}, house_name={house.house_name}, status={status.status}")

    return render_template(
        'house/house_detail.html',
        house=house,
        user=user,
        status=status,
        comments=enriched_comments,
        pagination=pagination
    )
# 新增房源管理路由
@house_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_house():
    if session.get('user_type') != 2:
        flash('只有房东可以发布房源', 'error')
        return redirect(url_for('account.landlord_home'))
    
    if request.method == 'GET':
        return render_template('house/add_house.html', cities_data=cities_data)
    
    # POST 请求处理
    try:
        # 获取表单数据
        house_name = request.form.get('house_name')
        rooms = request.form.get('rooms')
        province = request.form.get('province')
        city = request.form.get('city')
        district = request.form.get('district')
        addr = request.form.get('addr')
        price = request.form.get('price')
        deposit = request.form.get('deposit')
        situation = request.form.get('situation')
        highlight = request.form.get('highlight')
        phone = request.form.get('phone')
        
        # 组合地区信息
        region = f"{province}{city}{district}" if province and city and district else ""
        
        # 数据验证
        if not all([house_name, rooms, region, addr, price, phone]):
            flash('请填写必填信息', 'error')
            return render_template('house/add_house.html', cities_data=cities_data)
        
        # 处理图片上传
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # 生成唯一文件名
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"{timestamp}_{filename}"
                
                # 确保上传目录存在
                upload_folder = os.path.join(current_app.static_folder, 'images')
                os.makedirs(upload_folder, exist_ok=True)
                
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                image_path = f"static/images/{filename}"
        
        # 创建房源信息
        house_info = HouseInfoModel(
            house_name=house_name,
            rooms=rooms,
            region=region,
            addr=addr,
            price=float(price),
            deposit=float(deposit) if deposit else None,
            situation=situation,
            highlight=highlight,
            image=image_path
        )
        db.session.add(house_info)
        db.session.flush()  # 获取house_id
        
        # 创建房源状态（初始状态为2-装修中/未上架）
        house_status = HouseStatusModel(
            house_id=house_info.house_id,
            landlord_name=session.get('username'),
            status=2,  # 2表示装修中/未上架
            phone=phone,
            update_time=datetime.now()
        )
        db.session.add(house_status)
        db.session.commit()
        
        flash('房源发布成功！您可以申请上架供租客查看。', 'success')
        return redirect(url_for('account.landlord_home'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'发布失败：{str(e)}', 'error')
        return render_template('house/add_house.html', cities_data=cities_data)


@house_bp.route('/edit/<int:house_id>', methods=['GET', 'POST'])
@login_required
def edit_house(house_id):
    if session.get('user_type') != 2:
        flash('只有房东可以编辑房源', 'error')
        return redirect(url_for('account.landlord_home'))
    
    landlord_name = session.get('username')
    
    # 查找房源（确保是当前房东的房源）
    house_status = HouseStatusModel.query.filter_by(
        house_id=house_id, 
        landlord_name=landlord_name
    ).first()
    
    if not house_status:
        flash('房源不存在或您无权编辑', 'error')
        return redirect(url_for('account.landlord_home'))
    
    house_info = HouseInfoModel.query.get(house_id)
    if not house_info:
        flash('房源信息不存在', 'error')
        return redirect(url_for('account.landlord_home'))
    
    # 检查是否可以编辑（出租中的房源不允许编辑）
    if house_status.status == 1:
        flash('出租中的房源不允许编辑', 'error')
        return redirect(url_for('account.landlord_home'))
    
    if request.method == 'GET':
        return render_template('house/edit_house.html', 
                             house_info=house_info, 
                             house_status=house_status,
                             cities_data=cities_data)
    
    # POST 请求处理
    try:
        # 获取表单数据
        house_name = request.form.get('house_name')
        rooms = request.form.get('rooms')
        province = request.form.get('province')
        city = request.form.get('city')
        district = request.form.get('district')
        addr = request.form.get('addr')
        price = request.form.get('price')
        deposit = request.form.get('deposit')
        situation = request.form.get('situation')
        highlight = request.form.get('highlight')
        phone = request.form.get('phone')
        
        # 组合地区信息
        region = f"{province}{city}{district}" if province and city and district else house_info.region
        
        # 数据验证
        if not all([house_name, rooms, addr, price, phone]):
            flash('请填写必填信息', 'error')
            return render_template('house/edit_house.html', 
                                 house_info=house_info, 
                                 house_status=house_status,
                                 cities_data=cities_data)
        
        # 处理图片上传
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"{timestamp}_{filename}"
                
                upload_folder = os.path.join(current_app.static_folder, 'images')
                os.makedirs(upload_folder, exist_ok=True)
                
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                
                # 删除旧图片
                if house_info.image and os.path.exists(house_info.image):
                    try:
                        os.remove(house_info.image)
                    except:
                        pass
                
                house_info.image = f"static/images/{filename}"
        
        # 更新房源信息
        house_info.house_name = house_name
        house_info.rooms = rooms
        house_info.region = region
        house_info.addr = addr
        house_info.price = float(price)
        house_info.deposit = float(deposit) if deposit else None
        house_info.situation = situation
        house_info.highlight = highlight
        
        # 更新房源状态
        house_status.phone = phone
        house_status.update_time = datetime.now()
        
        db.session.commit()
        flash('房源信息更新成功！', 'success')
        return redirect(url_for('account.landlord_home'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'更新失败：{str(e)}', 'error')
        return render_template('house/edit_house.html', 
                             house_info=house_info, 
                             house_status=house_status,
                             cities_data=cities_data)


@house_bp.route('/delete/<int:house_id>', methods=['POST'])
@login_required
def delete_house(house_id):
    if session.get('user_type') != 2:
        return jsonify({'success': False, 'message': '只有房东可以删除房源'}), 403
    
    landlord_name = session.get('username')
    
    # 查找房源
    house_status = HouseStatusModel.query.filter_by(
        house_id=house_id, 
        landlord_name=landlord_name
    ).first()
    
    if not house_status:
        return jsonify({'success': False, 'message': '房源不存在或您无权删除'}), 404
    
    # 检查是否可以删除（出租中的房源不允许删除）
    if house_status.status == 1:
        return jsonify({'success': False, 'message': '出租中的房源不允许删除'}), 400
    
    try:
        # 删除图片文件
        house_info = HouseInfoModel.query.get(house_id)
        if house_info and house_info.image and os.path.exists(house_info.image):
            try:
                os.remove(house_info.image)
            except:
                pass
        
        # 删除相关记录（由于外键约束，会级联删除）
        db.session.delete(house_status)
        if house_info:
            db.session.delete(house_info)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '房源删除成功'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败：{str(e)}'}), 500


# 新闻管理
@house_bp.route('/news/add', methods=['GET', 'POST'])
@login_required
def add_news():
    if session.get('user_type') != 2:
        flash('只有房东可以发布新闻', 'error')
        return redirect(url_for('account.landlord_home'))
    
    # 获取房东的房源列表
    landlord_name = session.get('username')
    houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name).all()
    
    if request.method == 'GET':
        return render_template('house/add_news.html', houses=houses)
    
    # POST 请求处理
    try:
        house_id = request.form.get('house_id')
        title = request.form.get('title')
        desc = request.form.get('desc')
        
        if not all([house_id, title]):
            flash('请填写必填信息', 'error')
            return render_template('house/add_news.html', houses=houses)
        
        # 验证房源是否属于当前房东
        house_status = HouseStatusModel.query.filter_by(
            house_id=house_id, 
            landlord_name=landlord_name
        ).first()
        
        if not house_status:
            flash('房源不存在或您无权发布相关新闻', 'error')
            return render_template('house/add_news.html', houses=houses)
        
        # 创建新闻
        news = NewsModel(
            time=datetime.now(),
            house_id=house_id,
            title=title,
            desc=desc,
            landlord_username=landlord_name
        )
        db.session.add(news)
        db.session.commit()
        
        flash('新闻发布成功！', 'success')
        return redirect(url_for('house.manage_news'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'发布失败：{str(e)}', 'error')
        return render_template('house/add_news.html', houses=houses)


@house_bp.route('/news/manage')
@login_required
def manage_news():
    if session.get('user_type') != 2:
        flash('只有房东可以管理新闻', 'error')
        return redirect(url_for('account.landlord_home'))
    
    landlord_name = session.get('username')
    news_list = NewsModel.query.filter_by(landlord_username=landlord_name)\
                               .order_by(NewsModel.time.desc()).all()
    
    return render_template('house/manage_news.html', news_list=news_list)


# 维修请求管理
@house_bp.route('/repair/request', methods=['POST'])
@login_required
def create_repair_request():
    if session.get('user_type') != 1:  # 只有租客可以发起维修请求
        return jsonify({'success': False, 'message': '只有租客可以发起维修请求'}), 403
    
    try:
        house_id = request.json.get('house_id')
        content = request.json.get('content')
        
        if not all([house_id, content]):
            return jsonify({'success': False, 'message': '请填写维修内容'}), 400
        
        # 查找房源和房东
        house_status = HouseStatusModel.query.filter_by(house_id=house_id).first()
        if not house_status:
            return jsonify({'success': False, 'message': '房源不存在'}), 404
        
        # 创建维修请求
        repair_request = RepairRequestModel(
            house_id=house_id,
            tenant_username=session.get('username'),
            landlord_username=house_status.landlord_name,
            content=content
        )
        db.session.add(repair_request)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '维修请求已提交'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'提交失败：{str(e)}'}), 500


@house_bp.route('/repair/manage')
@login_required
def manage_repair_requests():
    if session.get('user_type') == 1:  # 租客查看自己发起的请求
        requests = RepairRequestModel.query.filter_by(
            tenant_username=session.get('username')
        ).order_by(RepairRequestModel.request_time.desc()).all()
        return render_template('house/tenant_repair_requests.html', requests=requests)
    
    elif session.get('user_type') == 2:  # 房东查看收到的请求
        requests = RepairRequestModel.query.filter_by(
            landlord_username=session.get('username')
        ).order_by(RepairRequestModel.request_time.desc()).all()
        return render_template('house/landlord_repair_requests.html', requests=requests)
    
    else:
        flash('无权访问', 'error')
        return redirect(url_for('index'))


@house_bp.route('/repair/handle/<int:request_id>', methods=['POST'])
@login_required
def handle_repair_request(request_id):
    if session.get('user_type') != 2:  # 只有房东可以处理
        return jsonify({'success': False, 'message': '只有房东可以处理维修请求'}), 403
    
    try:
        repair_request = RepairRequestModel.query.get(request_id)
        if not repair_request or repair_request.landlord_username != session.get('username'):
            return jsonify({'success': False, 'message': '维修请求不存在或您无权处理'}), 404
        
        status = request.json.get('status')
        notes = request.json.get('notes', '')
        
        if status not in ['已同意', '处理中', '已完成', '已拒绝']:
            return jsonify({'success': False, 'message': '无效的状态'}), 400
        
        repair_request.status = status
        repair_request.handler_notes = notes
        repair_request.handled_time = datetime.now()
        db.session.commit()
        
        return jsonify({'success': True, 'message': '处理成功'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'处理失败：{str(e)}'}), 500


# 保持原有的其他路由
@house_bp.route('/load_more_news', methods=['GET'])
def load_more_news():
    start = int(request.args.get('start', 0))
    limit = 7
    news_query = NewsModel.query.order_by(NewsModel.time.desc())
    news = news_query.offset(start).limit(limit).all()
    has_more = news_query.count() > start + limit
    news_data = [
        {
            'title': n.title,
            'desc': n.desc,
            'time': n.time.strftime('%Y-%m-%d')
        }
        for n in news
    ]
    return jsonify({'news': news_data, 'has_more': has_more})


@house_bp.route('/add_comment_form', methods=['POST'])
@login_required
def add_comment_form():
    house_id = request.form.get('house_id')
    desc = request.form.get('comment')
    at = request.form.get('at')
    user_type = session.get('user_type', 1)
    username = session.get('username')

    if not house_id or not desc or not username:
        return redirect(request.referrer or url_for('house.house_detail', house_id=house_id))

    comment = CommentModel(
        house_id=house_id,
        username=username,
        type=user_type,
        desc=desc,
        at=at,
        time=datetime.now()
    )
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('house.house_detail', house_id=house_id))


@house_bp.route('/appointment', methods=['POST'])
@login_required
def create_appointment():
    try:
        data = request.get_json()
        house_id = data.get('house_id')
        house_name = data.get('house_name')
        appointment_time = data.get('appointment_time')
        tenant_name = session.get('username')

        house = HouseInfoModel.query.filter_by(house_id=house_id).first()
        if not house:
            return jsonify({'code': 404, 'msg': '房屋不存在'}), 404

        house_status = HouseStatusModel.query.filter_by(house_id=house_id).first()
        if not house_status or not house_status.landlord_name:
            return jsonify({'code': 404, 'msg': '房东信息不存在'}), 404

        landlord_name = house_status.landlord_name

        try:
            appointment_time = datetime.strptime(appointment_time, '%Y-%m-%dT%H:%M')
        except ValueError:
            return jsonify({'code': 400, 'msg': '预约时间格式错误'}), 400

        appointment = AppointmentModel(
            house_id=house_id,
            house_name=house_name,
            tenant_name=tenant_name,
            landlord_name=landlord_name,
            appointment_time=appointment_time
        )
        db.session.add(appointment)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '预约已提交'})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'code': 500, 'msg': '服务器内部错误'}), 500


@house_bp.route('/appointments', methods=['GET'])
@login_required
def view_appointments():
    user_type = session.get('user_type')
    username = session.get('username')

    if user_type == 1:  # 租客
        appointments = AppointmentModel.query.filter_by(tenant_name=username).order_by(AppointmentModel.appointment_time.desc()).all()
    elif user_type == 2:  # 房东
        appointments = AppointmentModel.query.filter_by(landlord_name=username).order_by(AppointmentModel.appointment_time.desc()).all()
    else:
        return jsonify({'code': 403, 'msg': '无权限查看'}), 403

    return render_template('house/appointments.html', appointments=appointments)


@house_bp.route('/appointment/<int:appointment_id>/update', methods=['POST'])
@login_required
def update_appointment_status(appointment_id):
    data = request.get_json()
    status = data.get('status')

    appointment = AppointmentModel.query.filter_by(appointment_id=appointment_id).first()
    if not appointment:
        return jsonify({'code': 404, 'msg': '预约不存在'}), 404

    appointment.status = status
    db.session.commit()
    return jsonify({'code': 200, 'msg': '预约状态已更新'})


# 房源状态管理
@house_bp.route('/status/update/<int:house_id>', methods=['POST'])
@login_required
def update_house_status(house_id):
    """更新房源状态（房东操作）"""
    if session.get('user_type') != 2:
        return jsonify({'success': False, 'message': '只有房东可以更新房源状态'}), 403
    
    landlord_name = session.get('username')
    house_status = HouseStatusModel.query.filter_by(
        house_id=house_id, 
        landlord_name=landlord_name
    ).first()
    
    if not house_status:
        return jsonify({'success': False, 'message': '房源不存在或您无权操作'}), 404
    
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        # 状态验证
        if new_status not in [0, 1, 2]:
            return jsonify({'success': False, 'message': '无效的状态值'}), 400
        
        # 业务逻辑验证
        if house_status.status == 1 and new_status != 2:
            return jsonify({'success': False, 'message': '出租中的房源只能设置为装修中'}), 400
        
        house_status.status = new_status
        house_status.update_time = datetime.now()
        
        # 如果设置为出租中，可能需要创建租赁记录（这里简化处理）
        if new_status == 1:
            # 创建新闻通知
            news = NewsModel(
                time=datetime.now(),
                house_id=house_id,
                title=f"{house_status.house_info.house_name} 已出租",
                desc="该房源已成功出租，感谢您的关注！",
                landlord_username=landlord_name
            )
            db.session.add(news)
        
        db.session.commit()
        return jsonify({'success': True, 'message': '房源状态更新成功'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'更新失败：{str(e)}'}), 500


# 房源统计信息
@house_bp.route('/statistics')
@login_required
def house_statistics():
    """获取房源统计信息（房东）"""
    if session.get('user_type') != 2:
        flash('无权访问', 'error')
        return redirect(url_for('account.landlord_home'))
    
    landlord_name = session.get('username')
    
    # 统计各状态房源数量
    total_houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name).count()
    available_houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name, status=0).count()
    rented_houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name, status=1).count()
    unlisted_houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name, status=2).count()
    pending_houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name, status=4).count()
    
    # 近期维修请求
    recent_repairs = RepairRequestModel.query.filter_by(
        landlord_username=landlord_name,
        status='请求中'
    ).count()
    
    # 近期预约
    recent_appointments = AppointmentModel.query.filter_by(
        landlord_name=landlord_name,
        status='申请中'
    ).count()
    
    stats = {
        'total_houses': total_houses,
        'available_houses': available_houses,
        'rented_houses': rented_houses,
        'unlisted_houses': unlisted_houses,
        'pending_houses': pending_houses,
        'recent_repairs': recent_repairs,
        'recent_appointments': recent_appointments,
        'occupancy_rate': round((rented_houses / total_houses * 100), 2) if total_houses > 0 else 0
    }
    
    return render_template('house/statistics.html', stats=stats)


# 批量操作
@house_bp.route('/batch/action', methods=['POST'])
@login_required
def batch_house_action():
    """批量操作房源"""
    if session.get('user_type') != 2:
        return jsonify({'success': False, 'message': '只有房东可以进行批量操作'}), 403
    
    try:
        data = request.get_json()
        house_ids = data.get('house_ids', [])
        action = data.get('action')
        
        if not house_ids or not action:
            return jsonify({'success': False, 'message': '参数不完整'}), 400
        
        landlord_name = session.get('username')
        success_count = 0
        
        for house_id in house_ids:
            house_status = HouseStatusModel.query.filter_by(
                house_id=house_id,
                landlord_name=landlord_name
            ).first()
            
            if not house_status:
                continue
            
            if action == 'delete' and house_status.status != 1:
                # 删除房源
                house_info = HouseInfoModel.query.get(house_id)
                if house_info and house_info.image and os.path.exists(house_info.image):
                    try:
                        os.remove(house_info.image)
                    except:
                        pass
                db.session.delete(house_status)
                if house_info:
                    db.session.delete(house_info)
                success_count += 1
            
            elif action == 'apply_listing' and house_status.status in [2, 5]:
                # 批量申请上架
                house_status.status = 4
                house_status.update_time = datetime.now()
                
                # 创建审核记录
                audit = HouseListingAuditModel(
                    house_id=house_status.house_id,
                    house_name=house_status.house_info.house_name,
                    landlord_name=house_status.landlord_name,
                    audit_status=0
                )
                db.session.add(audit)
                success_count += 1
        
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': f'成功处理 {success_count} 个房源',
            'count': success_count
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'批量操作失败：{str(e)}'}), 500


# 房源搜索API
@house_bp.route('/api/search', methods=['GET'])
def api_house_search():
    """房源搜索API（支持前端AJAX调用）"""
    try:
        keyword = request.args.get('keyword', '').strip()
        region = request.args.get('region', '').strip()
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        rooms = request.args.get('rooms', '').strip()
        limit = request.args.get('limit', 10, type=int)
        
        # 构建查询
        query = HouseInfoModel.query.join(HouseStatusModel).filter(HouseStatusModel.status == 0)
        
        if keyword:
            query = query.filter(
                or_(
                    HouseInfoModel.house_name.like(f"%{keyword}%"),
                    HouseInfoModel.addr.like(f"%{keyword}%")
                )
            )
        
        if region:
            query = query.filter(HouseInfoModel.region.like(f"%{region}%"))
        
        if min_price is not None:
            query = query.filter(HouseInfoModel.price >= min_price)
        
        if max_price is not None:
            query = query.filter(HouseInfoModel.price <= max_price)
        
        if rooms:
            query = query.filter(HouseInfoModel.rooms.like(f"%{rooms}%"))
        
        houses = query.limit(limit).all()
        
        # 格式化返回数据
        results = []
        for house in houses:
            house_data = {
                'house_id': house.house_id,
                'house_name': house.house_name,
                'region': house.region,
                'addr': house.addr,
                'price': float(house.price),
                'rooms': house.rooms,
                'image': house.image,
                'url': url_for('house.house_detail', house_id=house.house_id)
            }
            results.append(house_data)
        
        return jsonify({
            'success': True,
            'data': results,
            'count': len(results)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'搜索失败：{str(e)}'
        }), 500


# 导出房源数据
@house_bp.route('/export')
@login_required
def export_houses():
    """导出房源数据（房东）"""
    if session.get('user_type') != 2:
        flash('无权访问', 'error')
        return redirect(url_for('account.landlord_home'))
    
    import csv
    from io import StringIO
    
    landlord_name = session.get('username')
    houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name).all()
    
    # 创建CSV内容
    output = StringIO()
    writer = csv.writer(output)
    
    # 写入表头
    writer.writerow([
        '房源ID', '房源名称', '户型', '地区', '详细地址', 
        '租金(元/月)', '押金(元)', '装修情况', '状态', '联系电话'
    ])
    
    # 写入数据
    for house in houses:
        house_info = house.house_info
        if house_info:
            status_map = {0: '已上架', 1: '出租中', 2: '未上架', 4: '待审核', 5: '审核未通过'}
            writer.writerow([
                house.house_id,
                house_info.house_name,
                house_info.rooms,
                house_info.region,
                house_info.addr,
                house_info.price,
                house_info.deposit or '',
                house_info.situation or '',
                status_map.get(house.status, '未知'),
                house.phone
            ])
    
    # 准备响应
    output.seek(0)
    
    from flask import Response
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename=houses_{landlord_name}_{datetime.now().strftime("%Y%m%d")}.csv'
        }
    )