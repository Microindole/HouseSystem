import csv
import json  # 添加这个导入
import os    # 也需要添加这个导入
import uuid  # 添加这个导入
from io import StringIO
from datetime import datetime
from flask import Response, g
from models import HouseStatusModel, db
from flask import render_template, request, jsonify, redirect, url_for, abort, flash, current_app, Response, g
from werkzeug.utils import secure_filename
from sqlalchemy import or_, text, and_
from models import (HouseInfoModel, HouseStatusModel, CommentModel, NewsModel,
                   TenantModel, LandlordModel, AppointmentModel, RepairRequestModel)
from service.logging import log_operation
# 新增导入 OSS 服务
from service.oss_service import get_oss_client, delete_oss_object
import alibabacloud_oss_v2 as oss_sdk

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def get_cities_data():
    with open('static/json/cities.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def get_house_list():
    try:
        region = request.args.get('region', '').strip()
        city = request.args.get('city', '').strip()
        keyword = request.args.get('keyword', '').strip()
        rooms = request.args.get('rooms', '').strip()
        address = request.args.get('address', '').strip()
        min_price = request.args.get('min_price', None, type=float)
        max_price = request.args.get('max_price', None, type=float)
        selected_region = region or ''
        selected_city = city or ''

        query = db.session.query(HouseInfoModel).join(
            HouseStatusModel,
            HouseInfoModel.house_id == HouseStatusModel.house_id
        ).filter(HouseStatusModel.status == 0)

        if address:
            query = query.filter(
                or_(
                    HouseInfoModel.addr.like(f"%{address}%"),
                    HouseInfoModel.region.like(f"%{address}%")
                )
            )

        if region:
            # 用 region 开头匹配，确保只包含该地区
            query = query.filter(HouseInfoModel.region.like(f"{region}%"))
        elif city:
            query = query.filter(HouseInfoModel.region.like(f"{city}%"))

        # 关键词过滤，不再重复地区条件
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

        query = query.order_by(HouseStatusModel.update_time.desc())

        page = request.args.get('page', 1, type=int)
        per_page = 9

        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        houses = pagination.items
        total_count = pagination.total  # 查询到的房屋总数

        news_list = NewsModel.query.order_by(NewsModel.time.desc()).limit(10).all()

        filters = {
            'region': selected_region,
            'city': selected_city,
            'keyword': keyword or '',
            'rooms': rooms or '',
            'min_price': min_price,
            'max_price': max_price,
            'address': address or ''
        }

        cities_data = get_cities_data()

        return render_template(
            'house/house_list.html',
            houses=houses,
            news_list=news_list,
            cities_data=cities_data,
            selected_region=selected_region,
            selected_city=selected_city,
            pagination=pagination,
            filters=filters,
            total_count=total_count  # 新增传递
        )

    except Exception as e:
        current_app.logger.error(f"房源列表页面错误: {str(e)}")
        import traceback
        traceback.print_exc()

        cities_data = get_cities_data()

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
            },
            total_count=0  # 异常时显示为0
        )


def get_house_detail(house_id):
    """获取房源详情并记录租客浏览历史"""
    house = HouseInfoModel.query.get(house_id)
    if not house:
        flash('房源不存在', 'error')
        abort(404)
    status = HouseStatusModel.query.filter_by(house_id=house_id).first()
    if not status:
        flash('房源状态信息不存在', 'error')
        abort(404)
    user_type = getattr(g, 'user_type', None)
    username = getattr(g, 'username', None)
    user = None
    if user_type == 1:
        user = TenantModel.query.filter_by(tenant_name=username).first()
    elif user_type == 2:
        user = LandlordModel.query.filter_by(landlord_name=username).first()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = CommentModel.query.filter_by(
        house_id=house_id
    ).order_by(
        CommentModel.time.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    comments_on_page = pagination.items
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
    
    # 记录租客浏览行为
    user_type = getattr(g, 'user_type', None)
    username = getattr(g, 'username', None)
    
    if user_type == 1 and username:  # 只记录租客浏览
        try:
            db.session.execute(text("CALL RecordTenantBrowse(:username, :house_id)"), 
                             {'username': username, 'house_id': house_id})
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"记录浏览历史失败: {str(e)}")
            db.session.rollback()
    
    current_app.logger.info(f"房源详情: house_id={house_id}, house_name={house.house_name}, status={status.status}")
    return render_template(
        'house/house_detail.html',
        house=house,
        user=user,
        status=status,
        comments=enriched_comments,
        pagination=pagination
    )

def export_houses_csv(landlord_name):
    """
    根据房东用户名导出房源数据为CSV格式的Response
    """
    houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        '房源ID', '房源名称', '户型', '地区', '详细地址',
        '租金(元/月)', '押金(元)', '装修情况', '状态', '联系电话'
    ])
    status_map = {0: '已上架', 1: '出租中', 2: '未上架', 4: '待审核', 5: '审核未通过'}
    for house in houses:
        house_info = house.house_info
        if house_info:
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
    output.seek(0)
    filename = f"houses_{landlord_name}_{datetime.now().strftime('%Y%m%d')}.csv"
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )

def upload_image_to_oss(file, house_id=None):
    """上传图片到OSS并返回URL"""
    try:
        client = get_oss_client()
        bucket_name = current_app.config['OSS_BUCKET_NAME']
        
        # 生成安全且唯一的文件名
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1]
        object_name = f"house_images/{house_id or 'temp'}/{uuid.uuid4().hex}{file_ext}"
        
        # 上传文件
        result = client.put_object(oss_sdk.PutObjectRequest(
            bucket=bucket_name,
            key=object_name,
            body=file.stream,
            headers={"x-oss-object-acl": "public-read"}
        ))
        
        if result.status_code == 200:
            # 构建图片URL
            oss_cname_url = current_app.config.get('OSS_CNAME_URL')
            if oss_cname_url:
                image_url = f"{oss_cname_url.rstrip('/')}/{object_name.lstrip('/')}"
            else:
                endpoint = current_app.config['OSS_ENDPOINT'].replace('https://', '').replace('http://', '')
                image_url = f"https://{bucket_name}.{endpoint}/{object_name}"
            
            return image_url
        else:
            raise Exception(f"OSS上传失败，状态码: {result.status_code}")
            
    except Exception as e:
        current_app.logger.error(f"OSS上传失败: {str(e)}")
        raise e

def add_house_logic():
    if getattr(g, 'user_type', None) != 2:
        flash('只有房东可以发布房源', 'error')
        return redirect(url_for('account.landlord_home'))
    cities_json_path = os.path.join(current_app.static_folder, 'json', 'cities.json')
    with open(cities_json_path, 'r', encoding='utf-8') as f:
        cities_data_for_provinces = json.load(f)
    pca_json_path = os.path.join(current_app.static_folder, 'json', 'pca-code.json')
    with open(pca_json_path, 'r', encoding='utf-8') as f:
        pca_data = json.load(f)
    if request.method == 'GET':
        return render_template('house/add_house.html',
                               cities_data=cities_data_for_provinces,
                               pca_data=pca_data)
    try:
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
        region = f"{province}{city}{district}" if province and city and district else ""
        if not all([house_name, rooms, region, addr, price, phone]):
            flash('请填写必填信息', 'error')
            return render_template('house/add_house.html',
                                   cities_data=cities_data_for_provinces,
                                   pca_data=pca_data)
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and allowed_file(file.filename):
                # 使用OSS上传替代本地存储
                image_url = upload_image_to_oss(file)
        
        house_info = HouseInfoModel(
            house_name=house_name,
            rooms=rooms,
            region=region,
            addr=addr,
            price=float(price),
            deposit=float(deposit) if deposit else None,
            situation=situation,
            highlight=highlight,
            image=image_url  # 保存OSS URL
        )
        db.session.add(house_info)
        db.session.flush()
        house_status = HouseStatusModel(
            house_id=house_info.house_id,
            landlord_name=g.username,
            status=2,
            phone=phone,
            update_time=datetime.now()
        )
        db.session.add(house_status)
        db.session.commit()
        log_operation(g.username, g.user_type, f"发布房源：{house_name}（位于 {region}）")
        flash('房源发布成功！您可以申请上架供租客查看。', 'success')
        return redirect(url_for('account.landlord_home'))
    except Exception as e:
        db.session.rollback()
        flash(f'发布失败：{str(e)}', 'error')
        return render_template('house/add_house.html',
                               cities_data=cities_data_for_provinces,
                               pca_data=pca_data)

def edit_house_logic(house_id):
    if getattr(g, 'user_type', None) != 2:
        flash('只有房东可以编辑房源', 'error')
        return redirect(url_for('account.landlord_home'))
    landlord_name = getattr(g, 'username', None)
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
    if house_status.status == 1:
        flash('出租中的房源不允许编辑', 'error')
        return redirect(url_for('account.landlord_home'))
    cities_data = get_cities_data()
    pca_json_path = os.path.join(current_app.static_folder, 'json', 'pca-code.json')
    with open(pca_json_path, 'r', encoding='utf-8') as f:
        pca_data = json.load(f)
    if request.method == 'GET':
        return render_template('house/edit_house.html',
                             house_info=house_info,
                             house_status=house_status,
                             cities_data=cities_data,
                             pca_data=pca_data)
    try:
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
        region = f"{province}{city}{district}" if province and city and district else house_info.region
        if not all([house_name, rooms, addr, price, phone]):
            flash('请填写必填信息', 'error')
            return render_template('house/edit_house.html',
                                 house_info=house_info,
                                 house_status=house_status,
                                 cities_data=cities_data,
                                 pca_data=pca_data)
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and allowed_file(file.filename):
                # 删除旧图片（如果是OSS URL）
                if house_info.image:
                    delete_oss_object(house_info.image)
                
                # 上传新图片到OSS
                house_info.image = upload_image_to_oss(file, house_id)
        house_info.house_name = house_name
        house_info.rooms = rooms
        house_info.region = region
        house_info.addr = addr
        house_info.price = float(price)
        house_info.deposit = float(deposit) if deposit else None
        house_info.situation = situation
        house_info.highlight = highlight
        house_status.phone = phone
        house_status.update_time = datetime.now()
        db.session.commit()
        log_operation(g.username, g.user_type, f"修改房源信息：{house_name}（ID: {house_id}，位于 {region}）")
        flash('房源信息更新成功！', 'success')
        return redirect(url_for('account.landlord_home'))
    except Exception as e:
        db.session.rollback()
        flash(f'更新失败：{str(e)}', 'error')
        return render_template('house/edit_house.html',
                             house_info=house_info,
                             house_status=house_status,
                             cities_data=cities_data,
                             pca_data=pca_data)

def delete_house_logic(house_id):
    if getattr(g, 'user_type', None) != 2:
        return jsonify({'success': False, 'message': '只有房东可以删除房源'}), 403
    landlord_name = getattr(g, 'username', None)
    house_status = HouseStatusModel.query.filter_by(
        house_id=house_id,
        landlord_name=landlord_name
    ).first()
    if not house_status:
        return jsonify({'success': False, 'message': '房源不存在或您无权删除'}), 404
    if house_status.status == 1:
        return jsonify({'success': False, 'message': '出租中的房源不允许删除'}), 400
    try:
        # 先删除新闻
        NewsModel.query.filter_by(house_id=house_id).delete()
        house_info = HouseInfoModel.query.get(house_id)
        
        # 删除OSS图片
        if house_info and house_info.image:
            delete_oss_object(house_info.image)
        
        db.session.delete(house_status)
        if house_info:
            db.session.delete(house_info)
        db.session.commit()
        log_operation(g.username, g.user_type, f"删除房源：ID {house_id}（房东：{landlord_name}）")
        return jsonify({'success': True, 'message': '房源删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败：{str(e)}'}), 500
    
def update_house_status_logic(house_id):
    """更新房源状态（房东操作）"""
    if getattr(g, 'user_type', None) != 2:
        return jsonify({'success': False, 'message': '只有房东可以更新房源状态'}), 403
    landlord_name = getattr(g, 'username', None)
    house_status = HouseStatusModel.query.filter_by(
        house_id=house_id,
        landlord_name=landlord_name
    ).first()
    if not house_status:
        return jsonify({'success': False, 'message': '房源不存在或您无权操作'}), 404
    try:
        data = request.get_json()
        new_status = data.get('status')
        if new_status not in [0, 1, 2]:
            return jsonify({'success': False, 'message': '无效的状态值'}), 400
        if house_status.status == 1 and new_status != 2:
            return jsonify({'success': False, 'message': '出租中的房源只能设置为装修中'}), 400
        house_status.status = new_status
        house_status.update_time = datetime.now()
        # 如果设置为出租中，创建新闻通知（简化处理）
        if new_status == 1:
            from models import NewsModel
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

def api_house_search_logic():
    """房源搜索API"""
    try:
        keyword = request.args.get('keyword', '').strip()
        region = request.args.get('region', '').strip()
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        rooms = request.args.get('rooms', '').strip()
        limit = request.args.get('limit', 10, type=int)
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

def get_tenant_browse_history(username, limit=20):
    """获取租客浏览历史"""
    try:
        result = db.session.execute(
            text("CALL GetTenantBrowseHistory(:username, :limit)"),
            {'username': username, 'limit': limit}
        )
        browse_list = result.fetchall()
        return browse_list
    except Exception as e:
        current_app.logger.error(f"获取浏览历史失败: {str(e)}")
        return []

def get_popular_houses_data(limit=10):
    """获取热门房源数据"""
    try:
        result = db.session.execute(
            text("CALL GetPopularHouses(:limit)"),
            {'limit': limit}
        )
        popular_houses = result.fetchall()
        return popular_houses
    except Exception as e:
        current_app.logger.error(f"获取热门房源失败: {str(e)}")
        return []

