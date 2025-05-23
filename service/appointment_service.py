from flask import request, jsonify, session, render_template
from datetime import datetime
from models import AppointmentModel, HouseInfoModel, HouseStatusModel, db

def create_appointment_logic():
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

def view_appointments_logic():
    user_type = session.get('user_type')
    username = session.get('username')
    if user_type == 1:
        appointments = AppointmentModel.query.filter_by(tenant_name=username).order_by(AppointmentModel.appointment_time.desc()).all()
    elif user_type == 2:
        appointments = AppointmentModel.query.filter_by(landlord_name=username).order_by(AppointmentModel.appointment_time.desc()).all()
    else:
        return jsonify({'code': 403, 'msg': '无权限查看'}), 403
    return render_template('house/appointments.html', appointments=appointments)

def update_appointment_status_logic(appointment_id):
    data = request.get_json()
    status = data.get('status')
    appointment = AppointmentModel.query.filter_by(appointment_id=appointment_id).first()
    if not appointment:
        return jsonify({'code': 404, 'msg': '预约不存在'}), 404
    appointment.status = status
    db.session.commit()
    return jsonify({'code': 200, 'msg': '预约状态已更新'})

