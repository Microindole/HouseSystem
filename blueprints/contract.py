# contract.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, g
from models import db, RentalContract, HouseInfoModel, PrivateChannelModel, HouseStatusModel
from datetime import datetime, timedelta
from functools import wraps
from decorators import verify_token

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
        contract_list.append({
            'house_name': house.house_name if house else '未知',
            'addr': house.addr if house else '未知',
            'landlord': contract.landlord_username,
            'tenant': contract.tenant_username,
            'amount': float(contract.total_amount),
            'start_time': contract.start_date,
            'end_time': contract.end_date,
            'status': contract.status,
            'contract_id': contract.id,
            'created_at': contract.created_at,
            'house_id': channel.house_id if channel else None,
            'house_status': house_status_obj.status if house_status_obj else None  # 新增
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