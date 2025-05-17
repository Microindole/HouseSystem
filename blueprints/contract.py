# contract.py
from flask import Blueprint, request, session, jsonify, render_template, redirect, url_for, flash
from models import db, RentalContract, HouseInfoModel, PrivateChannelModel
from datetime import datetime, timedelta
from functools import wraps

contract_bp = Blueprint('contract', __name__)

# 登录保护装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("请先登录", "error")
            return redirect(url_for('account.login'))
        return f(*args, **kwargs)
    return decorated_function




#展示交易历史（房东、租客都能看）
@contract_bp.route('/history')
@login_required
def view_contracts():
    username = session.get('username')
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

        contract_list.append({
            'house_name': house.house_name if house else '未知',
            'addr': house.addr if house else '未知',
            'landlord': contract.landlord_username,
            'tenant': contract.tenant_username,
            'amount': float(contract.total_amount),
            'start_date': contract.start_date,
            'end_date': contract.end_date,
            'status': contract.status,
            'contract_id': contract.id,
            'created_at': contract.created_at
        })

    return render_template('order/contract_history.html',
                           contracts=contract_list,
                           current_user=username,
                           page=page,
                           total_pages=total_pages)


@contract_bp.route('/cancel/<int:contract_id>', methods=['POST'])
@login_required
def cancel_contract(contract_id):
    username = session['username']
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