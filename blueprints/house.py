import json
import os
import uuid # Added for unique naming for OSS
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, abort, flash, current_app
from sqlalchemy import or_
from datetime import datetime
from models import (HouseInfoModel, HouseStatusModel, CommentModel, NewsModel,
                   TenantModel, LandlordModel, AppointmentModel, RepairRequestModel, db, HouseListingAuditModel) # Added HouseListingAuditModel
from decorators import login_required

# Imports for OSS integration (mimicking oss.py)
import alibabacloud_oss_v2 as oss_sdk
from alibabacloud_oss_v2.credentials import StaticCredentialsProvider


house_bp = Blueprint('house', __name__)

# 允许的图片扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load cities data once
cities_json_path_full = os.path.join(os.path.dirname(__file__), '..', 'static', 'json', 'cities.json')
pca_code_json_path_full = os.path.join(os.path.dirname(__file__), '..', 'static', 'json', 'pca-code.json')

try:
    with open(cities_json_path_full, 'r', encoding='utf-8') as f:
        cities_data_global = json.load(f)
except FileNotFoundError:
    cities_data_global = {} # Fallback if file not found during init
    current_app.logger.warning(f"Global cities.json not found at {cities_json_path_full}")


# --- OSS Helper Functions (Adapted from oss.py and extended) ---
def get_oss_client():
    """Initializes and returns an OSS client."""
    access_key_id = current_app.config.get('OSS_ACCESS_KEY_ID')
    access_key_secret = current_app.config.get('OSS_ACCESS_KEY_SECRET')
    endpoint = current_app.config.get('OSS_ENDPOINT')
    region = current_app.config.get('OSS_REGION')

    current_app.logger.info(
        f"OSS Config - ID Loaded: {'Yes' if access_key_id and access_key_id != 'YOUR_ACCESS_KEY_ID' else 'No/Default'}, Endpoint: {endpoint}, Region: {region}"
    )

    if not all([access_key_id, access_key_secret, endpoint]) or \
       access_key_id == "YOUR_ACCESS_KEY_ID" or access_key_secret == "YOUR_ACCESS_KEY_SECRET":
        msg = "OSS配置不完整或使用了默认占位符凭证。请检查应用的OSS配置。"
        current_app.logger.error(msg)
        raise ValueError(msg)

    credentials_provider = StaticCredentialsProvider(access_key_id, access_key_secret)
    
    cfg = oss_sdk.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.endpoint = endpoint
    if region: # e.g., 'cn-hangzhou'
        cfg.region = region
    
    return oss_sdk.Client(cfg)

def delete_oss_object(image_url):
    """Deletes an object from OSS given its full URL."""
    if not image_url or not image_url.startswith('http'):
        current_app.logger.info(f"Invalid or non-OSS URL, skipping deletion: {image_url}")
        return False
    
    try:
        bucket_name = current_app.config['OSS_BUCKET_NAME']
        oss_endpoint = current_app.config['OSS_ENDPOINT'] # e.g., oss-cn-hangzhou.aliyuncs.com
        oss_cname_url = current_app.config.get('OSS_CNAME_URL', '').rstrip('/')

        object_key = None
        # Try to parse from CNAME URL first
        if oss_cname_url and image_url.startswith(oss_cname_url + '/'):
            object_key = image_url.split(oss_cname_url + '/', 1)[1]
        else:
            # Try to parse from standard OSS URL (https://bucket.endpoint/key)
            # Ensure endpoint does not have http(s):// prefix for constructing the domain part
            endpoint_domain_part = oss_endpoint.replace('https://', '').replace('http://', '')
            standard_oss_url_prefix_https = f"https://{bucket_name}.{endpoint_domain_part}/"
            standard_oss_url_prefix_http = f"http://{bucket_name}.{endpoint_domain_part}/" # Less common but possible

            if image_url.startswith(standard_oss_url_prefix_https):
                object_key = image_url.split(standard_oss_url_prefix_https, 1)[1]
            elif image_url.startswith(standard_oss_url_prefix_http):
                object_key = image_url.split(standard_oss_url_prefix_http, 1)[1]

        if object_key:
            client = get_oss_client()
            current_app.logger.info(f"Attempting to delete OSS object: {object_key} from bucket {bucket_name}")
            req = oss_sdk.DeleteObjectRequest(bucket_name, object_key)
            client.delete_object(req)
            current_app.logger.info(f"Successfully deleted OSS object: {object_key}")
            return True
        else:
            # If it's an http/https URL but doesn't match known OSS patterns, log and skip
            current_app.logger.warning(f"Could not determine OSS object key from URL (might be a non-OSS URL or different format): {image_url}")
            return False
            
    except Exception as e:
        current_app.logger.error(f"Failed to delete OSS object {image_url}: {str(e)}")
        return False
# --- End OSS Helper Functions ---

@house_bp.route('', methods=['GET'])
def house_list():
    """房源列表页面 - 显示已上架的房源"""
    try:
        # 获取筛选条件
        region_filter = request.args.get('region', '').strip()
        city_filter = request.args.get('city', '').strip()
        keyword = request.args.get('keyword', '').strip()
        rooms = request.args.get('rooms', '').strip()
        address = request.args.get('address', '').strip()
        min_price = request.args.get('min_price', None, type=float)
        max_price = request.args.get('max_price', None, type=float)

        # 记录筛选条件
        selected_region = region_filter or ''
        selected_city = city_filter or ''

        query = db.session.query(HouseInfoModel).join(
            HouseStatusModel, 
            HouseInfoModel.house_id == HouseStatusModel.house_id
        ).filter(HouseStatusModel.status == 0)

        if address:
            query = query.filter(
                or_(
                    HouseInfoModel.addr.like(f"%{address}%"),
                    HouseInfoModel.region.like(f"%{address}%") # Keep this as it might contain specific districts
                )
            )
        
        # selected_region and selected_city come from nav, assume they are correct parts of the full region string
        if selected_region: # e.g. "北京市"
            query = query.filter(HouseInfoModel.region.like(f"%{selected_region}%"))
        if selected_city: # e.g. "北京市" or "朝阳区" depending on selection level
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
            room_filters = [HouseInfoModel.rooms.like(f"{i}室%") for i in range(4, 11)] # Check for 4室, 5室 etc.
            query = query.filter(or_(*room_filters))
        elif rooms: # e.g. "2室"
            query = query.filter(HouseInfoModel.rooms.like(f"{rooms}%"))


        if min_price is not None:
            query = query.filter(HouseInfoModel.price >= min_price)
        if max_price is not None:
            query = query.filter(HouseInfoModel.price <= max_price)

        query = query.order_by(HouseStatusModel.update_time.desc())

        page = request.args.get('page', 1, type=int)
        per_page = 9
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        houses_on_page = pagination.items

        news_list = NewsModel.query.order_by(NewsModel.time.desc()).limit(10).all()
        current_app.logger.info(f"房源列表查询: 找到{pagination.total}套房源, 第{page}页, 共{pagination.pages}页")

        filters = {
            'region': selected_region,
            'city': selected_city,
            'keyword': keyword or '',
            'rooms': rooms or '',
            'min_price': min_price,
            'max_price': max_price,
            'address': address or ''
        }
        
        # Use the globally loaded cities_data_global for the template context
        template_cities_data = cities_data_global

        return render_template(
            'house/house_list.html',
            houses=houses_on_page,
            news_list=news_list,
            cities_data=template_cities_data, # For nav dropdown if still needed there
            selected_region=selected_region,
            selected_city=selected_city,
            pagination=pagination,
            filters=filters
        )

    except Exception as e:
        current_app.logger.error(f"房源列表页面错误: {str(e)}")
        import traceback
        traceback.print_exc()
        template_cities_data = cities_data_global
        return render_template(
            'house/house_list.html', houses=[], news_list=[],
            cities_data=template_cities_data, selected_region='', selected_city='',
            pagination=None, filters={}
        )

@house_bp.route('/<int:house_id>', methods=['GET'])
def house_detail(house_id):
    house = HouseInfoModel.query.get(house_id)
    if not house:
        flash('房源不存在', 'error')
        abort(404)

    status = HouseStatusModel.query.filter_by(house_id=house_id).first()
    if not status:
        flash('房源状态信息不存在', 'error')
        abort(404)
    
    user_type = session.get('user_type')
    username = session.get('username')
    
    is_owner = user_type == 2 and status.landlord_name == username
    if not is_owner and status.status != 0: # Not owner and house not listed
        flash('该房源暂不可查看', 'error')
        return redirect(url_for('house.house_list'))
    
    user = None
    if username:
        if user_type == 1:
            user = TenantModel.query.filter_by(tenant_name=username).first()
        elif user_type == 2:
            user = LandlordModel.query.filter_by(landlord_name=username).first()
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = CommentModel.query.filter_by(house_id=house_id)\
                                   .order_by(CommentModel.time.desc())\
                                   .paginate(page=page, per_page=per_page, error_out=False)
    comments_on_page = pagination.items

    enriched_comments = []
    for comment in comments_on_page:
        comment_data = {
            'comment_id': comment.comment_id, 'username': comment.username,
            'type': comment.type, 'desc': comment.desc, 'time': comment.time,
            'at': comment.at, 'at_username': None, 'at_desc': None
        }
        if comment.at:
            at_comment = CommentModel.query.filter_by(comment_id=comment.at).first()
            if at_comment:
                comment_data['at_username'] = at_comment.username
                comment_data['at_desc'] = at_comment.desc
        enriched_comments.append(comment_data)

    current_app.logger.info(f"房源详情: house_id={house_id}, status={status.status}")
    return render_template('house/house_detail.html', house=house, user=user, status=status,
                           comments=enriched_comments, pagination=pagination)


@house_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_house():
    if session.get('user_type') != 2:
        flash('只有房东可以发布房源', 'error')
        return redirect(url_for('account.landlord_home'))

    try:
        with open(pca_code_json_path_full, 'r', encoding='utf-8') as f:
            pca_data_for_template = json.load(f)
    except FileNotFoundError:
        flash('地址数据加载失败，请联系管理员。', 'error')
        pca_data_for_template = {} # Fallback
        current_app.logger.error(f"pca-code.json not found at {pca_code_json_path_full}")


    if request.method == 'GET':
        return render_template('house/add_house.html', 
                               cities_data=pca_data_for_template, # For province dropdown based on pca_data keys
                               pca_data=pca_data_for_template)   # For JS logic

    # POST request
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
            flash('请填写所有必填信息（房源名称, 户型, 省市区, 详细地址, 月租金, 联系电话）', 'error')
            return render_template('house/add_house.html', cities_data=pca_data_for_template, pca_data=pca_data_for_template)

        oss_image_url = None # Will store the OSS URL
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and allowed_file(file.filename):
                try:
                    client = get_oss_client()
                    bucket_name = current_app.config['OSS_BUCKET_NAME']
                    
                    s_filename = secure_filename(file.filename)
                    file_ext = os.path.splitext(s_filename)[1]
                    # Using UUID for a unique object name in a general folder, not including house_id yet
                    object_name = f"house_images/{uuid.uuid4().hex}{file_ext}"

                    # Upload to OSS
                    req = oss_sdk.PutObjectRequest(
                        bucket=bucket_name,
                        key=object_name,
                        body=file.stream,
                        headers={"x-oss-object-acl": "public-read"} # Public read for images
                    )
                    client.put_object(req)

                    # Construct the image URL
                    oss_cname_url = current_app.config.get('OSS_CNAME_URL')
                    if oss_cname_url:
                        oss_image_url = f"{oss_cname_url.rstrip('/')}/{object_name.lstrip('/')}"
                    else:
                        endpoint_domain_part = current_app.config['OSS_ENDPOINT'].replace('https://', '').replace('http://', '')
                        oss_image_url = f"https://{bucket_name}.{endpoint_domain_part}/{object_name}"
                    current_app.logger.info(f"Image uploaded to OSS: {oss_image_url}")

                except ValueError as ve: # Handles get_oss_client config errors
                    flash(f'图片上传配置错误: {str(ve)}', 'error')
                    current_app.logger.error(f"OSS Config error during upload: {str(ve)}")
                except Exception as e:
                    current_app.logger.error(f"OSS Upload failed in add_house: {str(e)}")
                    flash(f'图片上传失败: {str(e)}', 'error')
                    # Decide if to proceed without image or return. Current: proceed, oss_image_url will be None.
        
        house_info = HouseInfoModel(
            house_name=house_name, rooms=rooms, region=region, addr=addr,
            price=float(price), deposit=float(deposit) if deposit else None,
            situation=situation, highlight=highlight, image=oss_image_url # Store OSS URL
        )
        db.session.add(house_info)
        db.session.flush()
        
        house_status = HouseStatusModel(
            house_id=house_info.house_id, landlord_name=session.get('username'),
            status=2, phone=phone, update_time=datetime.now()
        )
        db.session.add(house_status)
        db.session.commit()
        
        flash('房源发布成功！您可以申请上架供租客查看。', 'success')
        return redirect(url_for('account.landlord_home'))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in add_house POST: {str(e)}")
        flash(f'发布失败，发生内部错误：{str(e)}', 'error')
        return render_template('house/add_house.html', cities_data=pca_data_for_template, pca_data=pca_data_for_template)


@house_bp.route('/edit/<int:house_id>', methods=['GET', 'POST'])
@login_required
def edit_house(house_id):
    if session.get('user_type') != 2:
        flash('只有房东可以编辑房源', 'error')
        return redirect(url_for('account.landlord_home'))
    
    landlord_name = session.get('username')
    house_status = HouseStatusModel.query.filter_by(house_id=house_id, landlord_name=landlord_name).first()
    
    if not house_status:
        flash('房源不存在或您无权编辑', 'error')
        return redirect(url_for('account.landlord_home'))
    
    house_info = HouseInfoModel.query.get(house_id)
    if not house_info:
        flash('房源信息不存在', 'error') # Should not happen if status exists
        return redirect(url_for('account.landlord_home'))
    
    if house_status.status == 1: # 1 means rented
        flash('出租中的房源不允许编辑关键信息。如需修改，请先将房源状态调整为非出租状态。', 'warning')
        # Allow editing some fields or redirect, for now, let it proceed to form but with a warning

    template_cities_data = cities_data_global # Use global for consistency
    try:
        with open(pca_code_json_path_full, 'r', encoding='utf-8') as f:
            pca_data_for_template = json.load(f)
    except FileNotFoundError:
        flash('地址数据加载失败，部分功能可能受限。', 'warning')
        pca_data_for_template = {}


    if request.method == 'GET':
        return render_template('house/edit_house.html', 
                             house_info=house_info, house_status=house_status,
                             cities_data=template_cities_data, # For province options (keys of pca_data or separate list)
                             pca_data=pca_data_for_template) # For JS联动

    # POST request
    try:
        house_info.house_name = request.form.get('house_name')
        house_info.rooms = request.form.get('rooms')
        province = request.form.get('province')
        city = request.form.get('city')
        district = request.form.get('district')
        house_info.addr = request.form.get('addr')
        house_info.price = float(request.form.get('price'))
        deposit_str = request.form.get('deposit')
        house_info.deposit = float(deposit_str) if deposit_str else None
        house_info.situation = request.form.get('situation')
        house_info.highlight = request.form.get('highlight')
        house_status.phone = request.form.get('phone')
        
        house_info.region = f"{province}{city}{district}" if province and city and district else house_info.region
        
        if not all([house_info.house_name, house_info.rooms, house_info.addr, house_info.price, house_status.phone]):
            flash('请填写所有必填信息', 'error')
            return render_template('house/edit_house.html', house_info=house_info, house_status=house_status, cities_data=template_cities_data, pca_data=pca_data_for_template)
        
        # Handle image upload - replace old if new one is provided
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and allowed_file(file.filename):
                new_oss_image_url = None
                try:
                    client = get_oss_client()
                    bucket_name = current_app.config['OSS_BUCKET_NAME']
                    s_filename = secure_filename(file.filename)
                    file_ext = os.path.splitext(s_filename)[1]
                    object_name = f"house_images/{uuid.uuid4().hex}{file_ext}"

                    req = oss_sdk.PutObjectRequest(
                        bucket=bucket_name, key=object_name, body=file.stream,
                        headers={"x-oss-object-acl": "public-read"}
                    )
                    client.put_object(req)

                    oss_cname_url = current_app.config.get('OSS_CNAME_URL')
                    if oss_cname_url:
                        new_oss_image_url = f"{oss_cname_url.rstrip('/')}/{object_name.lstrip('/')}"
                    else:
                        endpoint_domain_part = current_app.config['OSS_ENDPOINT'].replace('https://', '').replace('http://', '')
                        new_oss_image_url = f"https://{bucket_name}.{endpoint_domain_part}/{object_name}"
                    
                    current_app.logger.info(f"New image uploaded to OSS: {new_oss_image_url}")

                    # Delete old image from OSS if it exists
                    if house_info.image:
                        delete_oss_object(house_info.image)
                    
                    house_info.image = new_oss_image_url # Update to new OSS URL

                except ValueError as ve:
                    flash(f'图片上传配置错误: {str(ve)}', 'error')
                    current_app.logger.error(f"OSS Config error during edit upload: {str(ve)}")
                except Exception as e:
                    current_app.logger.error(f"OSS Upload/Delete failed in edit_house: {str(e)}")
                    flash(f'图片处理失败: {str(e)}', 'error')
                    # Potentially don't update house_info.image if upload failed, or keep old one.
                    # Current logic: if upload fails, image field isn't updated to new, might keep old or be None if new_oss_image_url isn't set.
        
        house_status.update_time = datetime.now()
        db.session.commit()
        flash('房源信息更新成功！', 'success')
        return redirect(url_for('account.landlord_home'))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in edit_house POST: {str(e)}")
        flash(f'更新失败，发生内部错误：{str(e)}', 'error')
        return render_template('house/edit_house.html', house_info=house_info, house_status=house_status, cities_data=template_cities_data, pca_data=pca_data_for_template)


@house_bp.route('/delete/<int:house_id>', methods=['POST'])
@login_required
def delete_house(house_id):
    if session.get('user_type') != 2:
        return jsonify({'success': False, 'message': '只有房东可以删除房源'}), 403
    
    landlord_name = session.get('username')
    house_status = HouseStatusModel.query.filter_by(house_id=house_id, landlord_name=landlord_name).first()
    
    if not house_status:
        return jsonify({'success': False, 'message': '房源不存在或您无权删除'}), 404
    
    if house_status.status == 1: # Rented
        return jsonify({'success': False, 'message': '出租中的房源不允许删除'}), 400
    
    try:
        house_info = HouseInfoModel.query.get(house_id)
        if house_info and house_info.image:
            delete_oss_object(house_info.image) # Delete from OSS
        
        # Delete related records (comments, appointments etc. should be handled by cascade or explicitly if needed)
        CommentModel.query.filter_by(house_id=house_id).delete()
        AppointmentModel.query.filter_by(house_id=house_id).delete()
        RepairRequestModel.query.filter_by(house_id=house_id).delete()
        NewsModel.query.filter_by(house_id=house_id).delete() # News related to this house
        HouseListingAuditModel.query.filter_by(house_id=house_id).delete() # Audits for this house

        db.session.delete(house_status)
        if house_info:
            db.session.delete(house_info)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '房源删除成功'})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting house {house_id}: {str(e)}")
        return jsonify({'success': False, 'message': f'删除失败：{str(e)}'}), 500


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
        processed_ids = []
        
        for house_id_str in house_ids:
            try:
                house_id = int(house_id_str)
            except ValueError:
                current_app.logger.warning(f"Invalid house_id in batch action: {house_id_str}")
                continue

            house_status = HouseStatusModel.query.filter_by(
                house_id=house_id,
                landlord_name=landlord_name
            ).first()
            
            if not house_status:
                current_app.logger.warning(f"House status not found or no permission for house_id {house_id} in batch action.")
                continue
            
            if action == 'delete':
                if house_status.status == 1: # Rented
                    current_app.logger.info(f"Skipping deletion of rented house_id {house_id} in batch action.")
                    continue 
                
                house_info = HouseInfoModel.query.get(house_id)
                if house_info and house_info.image:
                    delete_oss_object(house_info.image) # Delete from OSS
                
                # Explicitly delete related items before house_info and house_status
                CommentModel.query.filter_by(house_id=house_id).delete()
                AppointmentModel.query.filter_by(house_id=house_id).delete()
                RepairRequestModel.query.filter_by(house_id=house_id).delete()
                NewsModel.query.filter_by(house_id=house_id).delete()
                HouseListingAuditModel.query.filter_by(house_id=house_id).delete()

                db.session.delete(house_status)
                if house_info:
                    db.session.delete(house_info)
                success_count += 1
                processed_ids.append(house_id)
            
            elif action == 'apply_listing':
                 if house_status.status in [2, 3, 5]: # 2: Unlisted/Decorating, 3: Taken Down, 5: Audit Rejected
                    house_status.status = 4 # 4: Pending Audit
                    house_status.update_time = datetime.now()
                    
                    # Create audit record if it doesn't exist or update existing one
                    audit = HouseListingAuditModel.query.filter_by(house_id=house_id).first()
                    if audit:
                        audit.audit_status = 0 # Pending
                        audit.request_time = datetime.now()
                        audit.audit_time = None
                        audit.audit_message = None
                    else:
                        audit = HouseListingAuditModel(
                            house_id=house_status.house_id,
                            house_name=house_status.house_info.house_name if house_status.house_info else "N/A",
                            landlord_name=house_status.landlord_name,
                            audit_status=0 # Pending
                        )
                        db.session.add(audit)
                    success_count += 1
                    processed_ids.append(house_id)
        
        if success_count > 0:
            db.session.commit()

        return jsonify({
            'success': True, 
            'message': f'成功处理 {success_count} 个房源。',
            'count': success_count,
            'processed_ids': processed_ids
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Batch action failed: {str(e)}")
        return jsonify({'success': False, 'message': f'批量操作失败：{str(e)}'}), 500

# --- Other routes remain unchanged, ensure they don't conflict with image handling ---
# (add_news, manage_news, delete_news, batch_delete_news, create_repair_request, etc.)
# ... (Rest of the house.py routes, assuming they don't directly interact with house image local paths)


# Placeholder for other routes from the original file.
# Ensure these routes are copied back if they were part of the original house.py
# For brevity, only image-related routes were heavily modified here.

@house_bp.route('/news/add', methods=['GET', 'POST'])
@login_required
def add_news():
    if session.get('user_type') != 2:
        flash('只有房东可以发布新闻', 'error')
        return redirect(url_for('account.landlord_home'))
    landlord_name = session.get('username')
    houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name).all() # Get houses for selection
    if request.method == 'GET':
        return render_template('house/add_news.html', houses=houses)
    try:
        house_id = request.form.get('house_id')
        title = request.form.get('title')
        desc = request.form.get('desc')
        if not all([house_id, title]):
            flash('请填写必填信息 (关联房源, 标题)', 'error')
            return render_template('house/add_news.html', houses=houses)
        
        # Validate house_id ownership
        house_check = HouseStatusModel.query.filter_by(house_id=house_id, landlord_name=landlord_name).first()
        if not house_check:
            flash('选择的房源无效或不属于您。', 'error')
            return render_template('house/add_news.html', houses=houses)

        news = NewsModel(
            time=datetime.now(), house_id=house_id, title=title, desc=desc,
            landlord_username=landlord_name
        )
        db.session.add(news)
        db.session.commit()
        flash('新闻发布成功！', 'success')
        return redirect(url_for('house.manage_news'))
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error adding news: {str(e)}")
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

@house_bp.route('/news/delete/<int:news_id>', methods=['POST'])
@login_required
def delete_news(news_id):
    if session.get('user_type') != 2:
        return jsonify({'success': False, 'message': '无权限'}), 403
    landlord_name = session.get('username')
    news = NewsModel.query.filter_by(id=news_id, landlord_username=landlord_name).first()
    if not news:
        return jsonify({'success': False, 'message': '新闻不存在或无权删除'}), 404
    try:
        db.session.delete(news)
        db.session.commit()
        return jsonify({'success': True, 'message': '新闻删除成功'})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting news {news_id}: {str(e)}")
        return jsonify({'success': False, 'message': f'删除失败：{str(e)}'}), 500

@house_bp.route('/news/batch-delete', methods=['POST'])
@login_required
def batch_delete_news():
    if session.get('user_type') != 2:
        return jsonify({'success': False, 'message': '无权限'}), 403
    try:
        data = request.get_json()
        news_ids = data.get('news_ids', [])
        if not news_ids:
            return jsonify({'success': False, 'message': '未选择任何新闻'}), 400
        landlord_name = session.get('username')
        deleted_count = 0
        for news_id_str in news_ids:
            try: news_id = int(news_id_str)
            except ValueError: continue
            news = NewsModel.query.filter_by(id=news_id, landlord_username=landlord_name).first()
            if news:
                db.session.delete(news)
                deleted_count += 1
        if deleted_count > 0:
            db.session.commit()
        return jsonify({'success': True, 'message': f'成功删除 {deleted_count} 条新闻', 'count': deleted_count})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error batch deleting news: {str(e)}")
        return jsonify({'success': False, 'message': f'批量删除失败：{str(e)}'}), 500

@house_bp.route('/repair/request', methods=['POST'])
@login_required
def create_repair_request():
    if session.get('user_type') != 1:
        return jsonify({'success': False, 'message': '只有租客可以发起维修请求'}), 403
    try:
        house_id = request.json.get('house_id')
        content = request.json.get('content')
        if not all([house_id, content]):
            return jsonify({'success': False, 'message': '请填写维修内容'}), 400
        house_status = HouseStatusModel.query.filter_by(house_id=house_id).first()
        if not house_status:
            return jsonify({'success': False, 'message': '房源不存在'}), 404
        repair_request = RepairRequestModel(
            house_id=house_id, tenant_username=session.get('username'),
            landlord_username=house_status.landlord_name, content=content
        )
        db.session.add(repair_request)
        db.session.commit()
        return jsonify({'success': True, 'message': '维修请求已提交'})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating repair request for house {house_id}: {str(e)}")
        return jsonify({'success': False, 'message': f'提交失败：{str(e)}'}), 500

@house_bp.route('/repair/manage')
@login_required
def manage_repair_requests():
    user_type = session.get('user_type')
    username = session.get('username')
    if user_type == 1:
        requests_list = RepairRequestModel.query.filter_by(tenant_username=username)\
                                         .order_by(RepairRequestModel.request_time.desc()).all()
        return render_template('house/tenant_repair_requests.html', requests=requests_list)
    elif user_type == 2:
        requests_list = RepairRequestModel.query.filter_by(landlord_username=username)\
                                         .order_by(RepairRequestModel.request_time.desc()).all()
        return render_template('house/landlord_repair_requests.html', requests=requests_list)
    else:
        flash('无权访问', 'error')
        return redirect(url_for('index'))

@house_bp.route('/repair/handle/<int:request_id>', methods=['POST'])
@login_required
def handle_repair_request(request_id):
    if session.get('user_type') != 2:
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
        current_app.logger.error(f"Error handling repair request {request_id}: {str(e)}")
        return jsonify({'success': False, 'message': f'处理失败：{str(e)}'}), 500

@house_bp.route('/load_more_news', methods=['GET'])
def load_more_news():
    start = int(request.args.get('start', 0))
    limit = 7 # Assuming this is how many you load per "more"
    news_query = NewsModel.query.order_by(NewsModel.time.desc())
    news_items = news_query.offset(start).limit(limit).all()
    has_more = news_query.count() > start + limit
    news_data = [{'title': n.title, 'desc': n.desc, 'time': n.time.strftime('%Y-%m-%d')} for n in news_items]
    return jsonify({'news': news_data, 'has_more': has_more})

@house_bp.route('/add_comment_form', methods=['POST'])
@login_required
def add_comment_form():
    house_id = request.form.get('house_id')
    desc = request.form.get('comment')
    at = request.form.get('at') # This is comment_id being replied to
    user_type = session.get('user_type', 1) # Default to tenant if not set, though login_required should ensure it
    username = session.get('username')
    if not all([house_id, desc, username]):
        return jsonify({'success': False, 'message': '缺少必要参数'}), 400
    try:
        comment = CommentModel(
            house_id=house_id, username=username, type=user_type,
            desc=desc, at=at if at else None, time=datetime.now()
        )
        db.session.add(comment)
        db.session.commit()
        return jsonify({'success': True, 'message': '评论发表成功'})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error adding comment for house {house_id}: {str(e)}")
        return jsonify({'success': False, 'message': f'评论发表失败: {str(e)}'}), 500

@house_bp.route('/appointment', methods=['POST'])
@login_required
def create_appointment():
    try:
        data = request.get_json()
        house_id = data.get('house_id')
        appointment_time_str = data.get('appointment_time')
        tenant_name = session.get('username')

        if not house_id or not appointment_time_str:
             return jsonify({'code': 400, 'msg': '缺少房屋ID或预约时间'}), 400

        house = HouseInfoModel.query.get(house_id)
        if not house:
            return jsonify({'code': 404, 'msg': '房屋不存在'}), 404
        
        house_status = HouseStatusModel.query.filter_by(house_id=house_id).first()
        if not house_status or not house_status.landlord_name:
            return jsonify({'code': 404, 'msg': '房东信息不存在或无法预约'}), 404
        
        if house_status.status != 0: # Not available for rent
            return jsonify({'code': 400, 'msg': '该房源当前不可预约看房'}), 400

        landlord_name = house_status.landlord_name
        try:
            appointment_time_dt = datetime.strptime(appointment_time_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            return jsonify({'code': 400, 'msg': '预约时间格式错误, 请使用 YYYY-MM-DDTHH:MM 格式'}), 400

        appointment = AppointmentModel(
            house_id=house_id, house_name=house.house_name, tenant_name=tenant_name,
            landlord_name=landlord_name, appointment_time=appointment_time_dt
        )
        db.session.add(appointment)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '预约已提交，请等待房东确认'})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating appointment for house {house_id}: {str(e)}")
        return jsonify({'code': 500, 'msg': f'服务器内部错误: {str(e)}'}), 500

@house_bp.route('/appointments', methods=['GET'])
@login_required
def view_appointments():
    user_type = session.get('user_type')
    username = session.get('username')
    appointments_list = []
    if user_type == 1:
        appointments_list = AppointmentModel.query.filter_by(tenant_name=username)\
                                           .order_by(AppointmentModel.appointment_time.desc()).all()
    elif user_type == 2:
        appointments_list = AppointmentModel.query.filter_by(landlord_name=username)\
                                           .order_by(AppointmentModel.appointment_time.desc()).all()
    else:
        return jsonify({'code': 403, 'msg': '无权限查看'}), 403 # Should be redirect or flash
    return render_template('house/appointments.html', appointments=appointments_list)

@house_bp.route('/appointment/<int:appointment_id>/update', methods=['POST'])
@login_required
def update_appointment_status(appointment_id):
    data = request.get_json()
    new_status = data.get('status') # e.g., "已确认", "已拒绝", "已完成"
    appointment = AppointmentModel.query.get(appointment_id)
    if not appointment:
        return jsonify({'code': 404, 'msg': '预约不存在'}), 404
    
    # Authorization: Only involved tenant or landlord can update (simplified: landlord confirms/rejects, tenant might cancel)
    username = session.get('username')
    user_type = session.get('user_type')

    can_update = False
    if user_type == 2 and appointment.landlord_name == username: # Landlord
        if new_status in ["已确认", "已拒绝", "已完成"]: can_update = True
    elif user_type == 1 and appointment.tenant_name == username: # Tenant
        if new_status == "已取消" and appointment.status == "申请中": can_update = True # Tenant can cancel pending
    
    if not can_update:
        return jsonify({'code': 403, 'msg': '无权限更新此预约的状态或状态无效'}), 403

    appointment.status = new_status
    db.session.commit()
    return jsonify({'code': 200, 'msg': '预约状态已更新'})

@house_bp.route('/status/update/<int:house_id>', methods=['POST'])
@login_required
def update_house_status(house_id):
    if session.get('user_type') != 2:
        return jsonify({'success': False, 'message': '只有房东可以更新房源状态'}), 403
    landlord_name = session.get('username')
    house_status = HouseStatusModel.query.filter_by(house_id=house_id, landlord_name=landlord_name).first()
    if not house_status:
        return jsonify({'success': False, 'message': '房源不存在或您无权操作'}), 404
    try:
        data = request.get_json()
        new_status_val = data.get('status')
        if new_status_val not in [0, 1, 2, 3]: # 0:上架, 1:出租中, 2:未上架/装修, 3:已下架
            return jsonify({'success': False, 'message': '无效的状态值'}), 400
        
        # Business logic, e.g., cannot directly set to 'rented' (1) from UI this way
        # This route might be for landlord manually taking it off market (3) or putting to unlisted (2)
        if house_status.status == 1 and new_status_val not in [2, 3]: # If rented, can only be set to unlisted or taken down
             return jsonify({'success': False, 'message': '出租中的房源只能设置为 "未上架" 或 "已下架"'}), 400

        house_status.status = new_status_val
        house_status.update_time = datetime.now()
        
        # If status changes to 'rented' or 'available', news might be generated elsewhere (e.g. contract signing)
        # For now, this just updates the status.
        db.session.commit()
        return jsonify({'success': True, 'message': '房源状态更新成功'})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating status for house {house_id}: {str(e)}")
        return jsonify({'success': False, 'message': f'更新失败：{str(e)}'}), 500

@house_bp.route('/statistics')
@login_required
def house_statistics():
    if session.get('user_type') != 2:
        flash('无权访问', 'error')
        return redirect(url_for('account.landlord_home'))
    landlord_name = session.get('username')
    
    base_query = HouseStatusModel.query.filter_by(landlord_name=landlord_name)
    total_houses = base_query.count()
    available_houses = base_query.filter_by(status=0).count()
    rented_houses = base_query.filter_by(status=1).count()
    unlisted_houses = base_query.filter_by(status=2).count() # Decorating/Unlisted
    taken_down_houses = base_query.filter_by(status=3).count() # Manually taken down
    pending_houses = base_query.filter_by(status=4).count() # Pending audit
    rejected_houses = base_query.filter_by(status=5).count() # Audit rejected

    recent_repairs_count = RepairRequestModel.query.filter_by(landlord_username=landlord_name, status='请求中').count()
    pending_appointments_count = AppointmentModel.query.filter_by(landlord_name=landlord_name, status='申请中').count()
    
    stats = {
        'total_houses': total_houses, 'available_houses': available_houses,
        'rented_houses': rented_houses, 'unlisted_houses': unlisted_houses,
        'taken_down_houses': taken_down_houses,
        'pending_houses': pending_houses, 'rejected_houses': rejected_houses,
        'recent_repairs': recent_repairs_count,
        'pending_appointments': pending_appointments_count,
        'occupancy_rate': round((rented_houses / total_houses * 100), 2) if total_houses > 0 else 0
    }
    return render_template('house/statistics.html', stats=stats)


@house_bp.route('/api/search', methods=['GET'])
def api_house_search():
    try:
        keyword = request.args.get('keyword', '').strip()
        region = request.args.get('region', '').strip()
        min_price_str = request.args.get('min_price')
        max_price_str = request.args.get('max_price')
        rooms = request.args.get('rooms', '').strip()
        limit = request.args.get('limit', 10, type=int)
        
        query = HouseInfoModel.query.join(HouseStatusModel).filter(HouseStatusModel.status == 0) # Only listed houses
        
        if keyword:
            query = query.filter(or_(HouseInfoModel.house_name.like(f"%{keyword}%"), HouseInfoModel.addr.like(f"%{keyword}%")))
        if region:
            query = query.filter(HouseInfoModel.region.like(f"%{region}%"))
        
        if min_price_str: query = query.filter(HouseInfoModel.price >= float(min_price_str))
        if max_price_str: query = query.filter(HouseInfoModel.price <= float(max_price_str))
        
        if rooms == '4室及以上':
            room_filters = [HouseInfoModel.rooms.like(f"{i}室%") for i in range(4, 11)]
            query = query.filter(or_(*room_filters))
        elif rooms:
            query = query.filter(HouseInfoModel.rooms.like(f"{rooms}%"))

        houses_result = query.limit(limit).all()
        results = []
        for house_item in houses_result:
            results.append({
                'house_id': house_item.house_id, 'house_name': house_item.house_name,
                'region': house_item.region, 'addr': house_item.addr,
                'price': float(house_item.price), 'rooms': house_item.rooms,
                'image': house_item.image or url_for('static', filename='images/default_house.png'), # Provide default if no image
                'url': url_for('house.house_detail', house_id=house_item.house_id, _external=True)
            })
        return jsonify({'success': True, 'data': results, 'count': len(results)})
    except Exception as e:
        current_app.logger.error(f"API house search error: {str(e)}")
        return jsonify({'success': False, 'message': f'搜索失败：{str(e)}'}), 500

@house_bp.route('/export')
@login_required
def export_houses():
    if session.get('user_type') != 2:
        flash('无权访问', 'error'); return redirect(url_for('account.landlord_home'))
    
    import csv
    from io import StringIO
    landlord_name = session.get('username')
    houses_statuses = HouseStatusModel.query.filter_by(landlord_name=landlord_name).all()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['房源ID', '房源名称', '户型', '地区', '详细地址', '租金(元/月)', '押金(元)', '装修情况', '状态', '联系电话', '图片URL'])
    
    status_map = {0: '已上架', 1: '出租中', 2: '未上架/装修中', 3: '已下架', 4: '待审核', 5: '审核未通过', None: '未知'}
    for hs in houses_statuses:
        hi = hs.house_info # HouseInfoModel related via backref or join
        if hi:
            writer.writerow([
                hs.house_id, hi.house_name, hi.rooms, hi.region, hi.addr,
                hi.price, hi.deposit or '', hi.situation or '',
                status_map.get(hs.status, '未知'), hs.phone, hi.image or ''
            ])
    output.seek(0)
    from flask import Response
    return Response(output.getvalue(), mimetype='text/csv',
                    headers={'Content-Disposition': f'attachment; filename=houses_export_{landlord_name}_{datetime.now().strftime("%Y%m%d")}.csv'})