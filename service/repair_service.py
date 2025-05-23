from flask import render_template, request, jsonify, session, flash, redirect, url_for, current_app
from datetime import datetime
from models import RepairRequestModel, HouseStatusModel, db

def create_repair_request_logic():
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

def manage_repair_requests_logic():
    user_type = session.get('user_type')
    username = session.get('username')
    if user_type == 1:
        requests = RepairRequestModel.query.filter_by(
            tenant_username=username
        ).order_by(RepairRequestModel.request_time.desc()).all()
        return render_template('house/tenant_repair_requests.html', requests=requests)
    elif user_type == 2:
        requests = RepairRequestModel.query.filter_by(
            landlord_username=username
        ).order_by(RepairRequestModel.request_time.desc()).all()
        return render_template('house/landlord_repair_requests.html', requests=requests)
    else:
        flash('无权访问', 'error')
        return redirect(url_for('index'))

def handle_repair_request_logic(request_id):
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
        return jsonify({'success': False, 'message': f'处理失败：{str(e)}'}), 500

