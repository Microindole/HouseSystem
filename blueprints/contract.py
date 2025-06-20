# contract.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, g
from models import (db, RentalContract, HouseInfoModel,
                    PrivateChannelModel, HouseStatusModel, ContractInfoModel, VisitStatsModel)
from datetime import datetime, timedelta
from functools import wraps
from decorators import verify_token
from sqlalchemy import func

contract_bp = Blueprint('contract', __name__)

# token登录保护装饰器

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('access_token')
        if not token:
            flash("请先登录", "error")
            return redirect(url_for('account.login'))
        payload = verify_token(token)
        if not payload:
            flash("登录已过期，请重新登录", "error")
            return redirect(url_for('account.login'))
        g.username = payload.get('username')
        g.user_type = payload.get('user_type')
        return f(*args, **kwargs)
    return decorated_function




#展示交易历史（房东、租客都能看）


@contract_bp.route('/history')
@login_required
def view_contracts():
    username = g.username
    page = request.args.get('page', 1, type=int)
    per_page = 9  # 每页显示9条

    # 查询用户相关合同，分页
    pagination = RentalContract.query.filter(
        (RentalContract.landlord_username == username) |
        (RentalContract.tenant_username == username)
    ).order_by(RentalContract.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    contracts = pagination.items
    total_pages = pagination.pages

    contract_list = []
    for contract in contracts:
        channel = PrivateChannelModel.query.get(contract.channel_id)
        house = HouseInfoModel.query.get(channel.house_id) if channel else None
        house_status_obj = None
        if channel:
            house_status_obj = HouseStatusModel.query.filter_by(
                house_id=channel.house_id,
                landlord_name=contract.landlord_username
            ).first()

        # 获取合同详情信息
        contract_info = ContractInfoModel.query.filter_by(rental_contract_id=contract.id).first()
        contract_agreed = False
        if contract_info and contract_info.tenant_signature_identifier:
            contract_agreed = True

        def add_8_hours(dt):
            if dt:
                return dt + timedelta(hours=8)
            return None

        contract_list.append({
            'house_name': house.house_name if house else '未知',
            'addr': house.addr if house else '未知',
            'landlord': contract.landlord_username,
            'tenant': contract.tenant_username,
            'amount': float(contract.total_amount),
             'start_time': add_8_hours(contract.start_date),
            'end_time': add_8_hours(contract.end_date),
            'status': contract.status,
            'contract_id': contract.id,
            'created_at': add_8_hours(contract.created_at),
            'house_id': channel.house_id if channel else None,
            'house_status': house_status_obj.status if house_status_obj else None,
            'contract_agreed': contract_agreed,  # 是否已同意合同
            'contract_document_url': url_for('contract.view_contract', contract_id=contract.id)  # 合同查看URL
        })

    return render_template('order/contract_history.html',
                           contracts=contract_list,
                           current_user=username,
                           page=page,
                           total_pages=total_pages)


@contract_bp.route('/cancel/<int:contract_id>', methods=['POST'])
@login_required
def cancel_contract(contract_id):
    username = g.username
    contract = RentalContract.query.get(contract_id)

    if not contract:
        flash("合同不存在", "error")
        return redirect(url_for('contract.view_contracts'))

    if contract.landlord_username != username:
        flash("无权限撤销该合同", "error")
        return redirect(url_for('contract.view_contracts'))

    if contract.status != 0:
        flash("该合同无法撤销", "error")
        return redirect(url_for('contract.view_contracts'))

    contract.status = 3  # 撤销状态
    db.session.commit()
    flash("合同已撤销", "success")
    return redirect(url_for('contract.view_contracts'))


@contract_bp.route('/return/<int:contract_id>', methods=['POST'])
@login_required
def return_house(contract_id):
    contract = RentalContract.query.get_or_404(contract_id)
    username = g.username
    # 只有租客本人能归还
    if contract.tenant_username != username:
        flash("无权限归还该房屋", "error")
        return redirect(url_for('contract.view_contracts'))

    # 找到对应房屋状态
    channel = PrivateChannelModel.query.get(contract.channel_id)
    if not channel:
        flash("找不到对应频道", "error")
        return redirect(url_for('contract.view_contracts'))

    house_status = HouseStatusModel.query.filter_by(
        house_id=channel.house_id,
        landlord_name=contract.landlord_username
    ).first()
    if not house_status:
        flash("找不到房屋状态", "error")
        return redirect(url_for('contract.view_contracts'))

    house_status.status = 2  # 2为装修中
    db.session.commit()
    flash("归还成功，房屋状态已设为装修中", "success")
    return redirect(url_for('contract.view_contracts'))


@contract_bp.route('/api/income/cancel_stats')
@login_required
def cancel_income_stats():
    start_str = request.args.get('start_date')
    end_str = request.args.get('end_date')

    # 默认最近七天
    if not start_str or not end_str:
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=6)
    else:
        start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_str, '%Y-%m-%d').date()

    results = db.session.query(
        func.date(RentalContract.updated_at).label('date'),
        func.count(RentalContract.id).label('order_count'),
        func.sum(RentalContract.total_amount).label('total_amount')
    ).filter(
        RentalContract.status == 4,
        RentalContract.updated_at >= start_date,
        RentalContract.updated_at <= end_date + timedelta(days=1)
    ).group_by(
        func.date(RentalContract.updated_at)
    ).order_by(
        func.date(RentalContract.updated_at)
    ).all()

    data = [
        {
            "date": row.date.strftime('%Y-%m-%d'),
            "order_count": row.order_count,
            "total_amount": float(row.total_amount or 0)
        }
        for row in results
    ]
    return jsonify(data)

# routes/stats.py（或者你的蓝图中）
@contract_bp.route('/api/visit/stats')
@login_required
def get_visit_stats():
    stats = VisitStatsModel.query.order_by(VisitStatsModel.visit_date).all()
    data = [
        {
            'date': s.visit_date.strftime('%Y-%m-%d'),
            'visits': s.unique_visits
        } for s in stats
    ]
    return jsonify(data)


@contract_bp.route('/view_contract/<int:contract_id>')
@login_required
def view_contract(contract_id):
    """查看合同文档"""
    contract = RentalContract.query.get_or_404(contract_id)

    # 检查权限 - 只有合同的相关方才能查看
    if g.username not in [contract.landlord_username, contract.tenant_username]:
        flash('您没有权限查看此合同', 'danger')
        return redirect(url_for('contract.view_contracts'))

    # 获取合同详情
    contract_info = ContractInfoModel.query.filter_by(rental_contract_id=contract_id).first()

    # 获取房屋信息
    channel = PrivateChannelModel.query.get(contract.channel_id)
    house = None
    landlord_phone = None
    tenant_phone = None
    house_status = None

    if channel:
        house = HouseInfoModel.query.get(channel.house_id)
        house_status = HouseStatusModel.query.filter_by(
            house_id=channel.house_id,
            landlord_name=contract.landlord_username
        ).first()

        # 获取房东和租客的联系方式
        from models import LandlordModel, TenantModel
        landlord = LandlordModel.query.filter_by(landlord_name=contract.landlord_username).first()
        if landlord:
            landlord_phone = landlord.phone

        tenant = TenantModel.query.filter_by(tenant_name=contract.tenant_username).first()
        if tenant:
            tenant_phone = tenant.phone

    # 如果没有合同详情信息，自动创建一个
    if not contract_info and house:
        # 安全地获取押金金额
        deposit = 0
        if house.deposit is not None:
            try:
                deposit = float(house.deposit)
            except (ValueError, TypeError):
                deposit = 0

        # 格式化房屋详情信息，包含更多细节
        parking_info = "有" if hasattr(house, 'has_parking_lot') and house.has_parking_lot else "无"
        area_str = f"{house.area}" if house and hasattr(house, 'area') and house.area else "未提供"
        floor_info = ""
        if hasattr(house, 'floor') and hasattr(house, 'floor_all') and house.floor and house.floor_all:
            floor_info = f"{house.floor}/{house.floor_all}层"
        elif hasattr(house, 'floor') and house.floor:
            floor_info = f"{house.floor}层"
        else:
            floor_info = "未提供"

        house_details = f"""
房屋坐落于{house.region or ''}，{house.addr or '未提供具体地址'}，
房屋权属：产权清晰，甲方拥有合法出租权，
建筑面积约{area_str}平方米，
户型：{house.rooms or '未提供户型'}，
所在楼层：{floor_info}，
装修状况：{house.situation or '普通装修'}，
配套设施：{house.highlight or '常规家具家电配套'}；
车位信息：{parking_info}；
其他描述：房屋状态良好，水电气暖设施齐全，符合正常居住条件。"""

        contract_info = ContractInfoModel(
            rental_contract_id=contract_id,
            contract_document_id=f"GF—2025—{contract_id}",
            house_details_text_snapshot=house_details.strip(),
            lease_purpose_text="居住",
            rent_payment_frequency="月付",
            deposit_amount_numeric_snapshot=deposit,  # 使用从house_info表获取的押金数据
            info_created_at=datetime.utcnow(),
            info_updated_at=datetime.utcnow()
        )
        try:
            db.session.add(contract_info)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # 出错时创建一个临时对象，不保存到数据库
            contract_info = ContractInfoModel(
                rental_contract_id=contract_id,
                contract_document_id="GF—2025—临时",
                house_details_text_snapshot="暂无详细信息，请联系管理员",
                lease_purpose_text="居住",
                rent_payment_frequency="月付",
                deposit_amount_numeric_snapshot=0
            )

    # 将合同信息传递给模板
    return render_template(
        'order/contract_document.html',
        contract=contract,
        contract_info=contract_info,
        house=house,
        house_status=house_status,
        landlord_username_placeholder=contract.landlord_username,
        tenant_username_placeholder=contract.tenant_username,
        landlord_phone_placeholder=landlord_phone or "未提供",
        tenant_phone_placeholder=tenant_phone or "未提供"
    )

@contract_bp.route('/sign_contract_page/<int:contract_id>')
@login_required
def sign_contract_page(contract_id):
    """租客签署合同页面"""
    # 获取合同信息
    contract = RentalContract.query.get_or_404(contract_id)

    # 检查权限 - 只有合同的租客才能签署
    if g.username != contract.tenant_username:
        flash('只有租客才能签署此合同', 'danger')
        return redirect(url_for('contract.view_contracts'))

    # 获取合同详情
    contract_info = ContractInfoModel.query.filter_by(rental_contract_id=contract_id).first()

    # 获取房源信息
    channel = PrivateChannelModel.query.get(contract.channel_id)
    house = None
    landlord_phone = None
    tenant_phone = None
    house_status = None

    if channel:
        house = HouseInfoModel.query.get(channel.house_id)
        house_status = HouseStatusModel.query.filter_by(
            house_id=channel.house_id,
            landlord_name=contract.landlord_username
        ).first()

        # 获取房东和租客的联系方式
        from models import LandlordModel, TenantModel
        landlord = LandlordModel.query.filter_by(landlord_name=contract.landlord_username).first()
        if landlord:
            landlord_phone = landlord.phone

        tenant = TenantModel.query.filter_by(tenant_name=contract.tenant_username).first()
        if tenant:
            tenant_phone = tenant.phone

    # 如果没有合同详情，自动创建一个初始化版本
    if not contract_info and house:
        # 安全地获取押金金额
        deposit = 0
        if house.deposit is not None:
            try:
                deposit = float(house.deposit)
            except (ValueError, TypeError):
                deposit = 0

        # 格式化房屋详情信息，与view_contract保持一致
        parking_info = "有" if hasattr(house, 'has_parking_lot') and house.has_parking_lot else "无"
        area_str = f"{house.area}" if house and hasattr(house, 'area') and house.area else "未提供"
        floor_info = ""
        if hasattr(house, 'floor') and hasattr(house, 'floor_all') and house.floor and house.floor_all:
            floor_info = f"{house.floor}/{house.floor_all}层"
        elif hasattr(house, 'floor') and house.floor:
            floor_info = f"{house.floor}层"
        else:
            floor_info = "未提供"

        house_details = f"""
房屋坐落于{house.region or ''}，{house.addr or '未提供具体地址'}，
房屋权属：产权清晰，甲方拥有合法出租权，
建筑面积约{area_str}平方米，
户型：{house.rooms or '未提供户型'}，
所在楼层：{floor_info}，
装修状况：{house.situation or '普通装修'}，
配套设施：{house.highlight or '常规家具家电配套'}；
车位信息：{parking_info}；
其他描述：房屋状态良好，水电气暖设施齐全，符合正常居住条件。"""

        contract_info = ContractInfoModel(
            rental_contract_id=contract_id,
            contract_document_id=f"GF—2025—{contract_id}",
            house_details_text_snapshot=house_details.strip(),
            lease_purpose_text="居住",
            rent_payment_frequency="月付",
            deposit_amount_numeric_snapshot=deposit,
            info_created_at=datetime.utcnow(),
            info_updated_at=datetime.utcnow()
        )
        try:
            db.session.add(contract_info)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # 出错时不阻止页面显示，而是返回一个临时对象
            contract_info = ContractInfoModel(
                rental_contract_id=contract_id,
                contract_document_id="GF—2025—临时",
                house_details_text_snapshot="暂无详细信息，请联系管理员",
                lease_purpose_text="居住",
                rent_payment_frequency="月付",
                deposit_amount_numeric_snapshot=0
            )

    # 将必要信息传递给模板
    return render_template(
        'order/sign_contract.html',
        contract=contract,
        contract_info=contract_info,
        house=house,
        house_status=house_status,
        landlord_username_placeholder=contract.landlord_username,
        tenant_username_placeholder=contract.tenant_username,
        landlord_phone_placeholder=landlord_phone or "未提供",
        tenant_phone_placeholder=tenant_phone or "未提供"
    )

@contract_bp.route('/sign_contract/<int:contract_id>', methods=['POST'])
@login_required
def sign_contract(contract_id):
    """处理租客签署合同请求"""
    contract = RentalContract.query.get_or_404(contract_id)

    # 检查权限 - 只有租客才能签署
    if g.username != contract.tenant_username:
        return jsonify(success=False, message='只有租客才能签署此合同')

    # 获取合同详情
    contract_info = ContractInfoModel.query.filter_by(rental_contract_id=contract_id).first()
    if not contract_info:
        # 如果找不到合同详情，创建一个基本的合同详情记录
        channel = PrivateChannelModel.query.get(contract.channel_id)
        house = None
        house_status = None
        deposit = 0  # 默认押金为0

        if channel:
            house = HouseInfoModel.query.get(channel.house_id)
            house_status = HouseStatusModel.query.filter_by(
                house_id=channel.house_id,
                landlord_name=contract.landlord_username
            ).first()

            # 安全地获取押金金额 - 从house_info表获取
            if house and house.deposit is not None:
                try:
                    deposit = float(house.deposit)
                except (ValueError, TypeError):
                    deposit = 0

        # 生成更详细的房屋描述
        house_details = "房屋基本信息未详细提供"
        if house:
            # 格式化房屋详情信息
            parking_info = "有" if hasattr(house, 'has_parking_lot') and house.has_parking_lot else "无"
            area_str = f"{house.area}" if house and hasattr(house, 'area') and house.area else "未提供"
            floor_info = ""
            if hasattr(house, 'floor') and hasattr(house, 'floor_all') and house.floor and house.floor_all:
                floor_info = f"{house.floor}/{house.floor_all}层"
            elif hasattr(house, 'floor') and house.floor:
                floor_info = f"{house.floor}层"
            else:
                floor_info = "未提供"

            house_details = f"""
房屋坐落于{house.region or ''}，{house.addr or '未提供具体地址'}，
房屋权属：产权清晰，甲方拥有合法出租权，
建筑面积约{area_str}平方米，
户型：{house.rooms or '未提供户型'}，
所在楼层：{floor_info}，
装修状况：{house.situation or '普通装修'}，
配套设施：{house.highlight or '常规家具家电配套'}；
车位信息：{parking_info}；
其他描述：房屋状态良好，水电气暖设施齐全，符合正常居住条件。"""

        contract_info = ContractInfoModel(
            rental_contract_id=contract_id,
            contract_document_id=f"GF—2025—{contract_id}",
            house_details_text_snapshot=house_details.strip(),
            lease_purpose_text="居住",
            rent_payment_frequency="月付",
            deposit_amount_numeric_snapshot=deposit,
            info_created_at=datetime.utcnow(),
            info_updated_at=datetime.utcnow()
        )
        db.session.add(contract_info)

    # 更新签名信息
    now = datetime.utcnow() + timedelta(hours=8)  # 北京时间
    contract_info.tenant_signature_identifier = g.username
    contract_info.tenant_signature_datetime = now
    contract_info.info_updated_at = now

    # 修改：更新合同状态为"已签署待支付"
    contract.status = 1  # 已签署待支付状态

    try:
        db.session.commit()
        return jsonify(success=True, message='合同已成功签署！您现在可以进行支付。')
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=f'签署合同时发生错误: {str(e)}')

@contract_bp.route('/upload_contract_page/<int:contract_id>')
@login_required
def upload_contract_page(contract_id):
    """房东编辑/上传合同页面"""
    contract = RentalContract.query.get_or_404(contract_id)

    # 检查权限 - 只有房东才能编辑
    if g.username != contract.landlord_username:
        flash('只有房东才能编辑此合同', 'danger')
        return redirect(url_for('contract.view_contracts'))

    # 获取合同详情
    contract_info = ContractInfoModel.query.filter_by(rental_contract_id=contract_id).first()

    # 获取房源信息
    channel = PrivateChannelModel.query.get(contract.channel_id)
    house = None
    if channel:
        house = HouseInfoModel.query.get(channel.house_id)

    return render_template(
        'order/contract_document.html',
        contract=contract,
        contract_info=contract_info,
        house=house,
        edit_mode=True,
        landlord_username_placeholder=contract.landlord_username,
        tenant_username_placeholder=contract.tenant_username
    )

@contract_bp.route('/cancel_signing/<int:contract_id>', methods=['GET', 'POST'])
@login_required
def cancel_signing(contract_id):
    """租客取消签署合同"""
    contract = RentalContract.query.get_or_404(contract_id)

    # 检查权限 - 只有租客才能取消签署
    if g.username != contract.tenant_username:
        if request.method == 'POST':
            return jsonify(success=False, message='只有租客才能取消签署此合同')
        else:
            flash('只有租客才能取消签署此合同', 'danger')
            return redirect(url_for('contract.view_contracts'))

    # 更新合同状态为 "已取消"
    contract.status = 2  # 修改：按照注释说明，2表示"已取消"

    try:
        db.session.commit()
        if request.method == 'POST':
            return jsonify(success=True, message='您已取消签署合同，房东可能会重新发起合同。')
        else:
            flash('您已取消签署合同，房东可能会重新发起合同。', 'info')
            return redirect(url_for('contract.view_contracts'))
    except Exception as e:
        db.session.rollback()
        if request.method == 'POST':
            return jsonify(success=False, message=f'取消签署时发生错误: {str(e)}')
        else:
            flash(f'取消签署时发生错误: {str(e)}', 'danger')
            return redirect(url_for('contract.view_contracts'))

@contract_bp.route('/create_new_contract')
@login_required
def create_new_contract():
    """房东针对同一租客和房源发起新合同"""
    house_id = request.args.get('house_id')
    tenant = request.args.get('tenant')

    if not house_id or not tenant:
        flash('参数不完整', 'error')
        return redirect(url_for('contract.view_contracts'))

    # 检查权限 - 只有房东才能发起
    house_status = HouseStatusModel.query.filter_by(house_id=house_id, landlord_name=g.username).first()
    if not house_status:
        flash('您没有权限为此房源发起合同', 'error')
        return redirect(url_for('contract.view_contracts'))

    # 创建新合同
    channel = PrivateChannelModel.query.filter_by(house_id=house_id, tenant_username=tenant).first()
    if not channel:
        # 如果没有找到已存在的私聊频道，创建一个新的
        channel = PrivateChannelModel(
            house_id=house_id,
            landlord_username=g.username,
            tenant_username=tenant,
            created_at=datetime.utcnow()
        )
        db.session.add(channel)
        db.session.commit()

    # 获取房源信息以获取租金金额
    house = HouseInfoModel.query.get_or_404(house_id)

    # 创建新合同
    new_contract = RentalContract(
        landlord_username=g.username,
        tenant_username=tenant,
        channel_id=channel.channel_id,  # 修改：使用 channel_id 而不是 id
        total_amount=house.price if house.price else 0,
        status=0,  # 初始状态：待签署
        start_date=datetime.utcnow() + timedelta(days=1),  # 默认从明天开始
        end_date=datetime.utcnow() + timedelta(days=366),  # 默认一年租期
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    try:
        db.session.add(new_contract)
        db.session.commit()
        flash('新合同已发起，等待租客签署', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'创建新合同时发生错误: {str(e)}', 'danger')

    return redirect(url_for('contract.view_contracts'))