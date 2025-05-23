import os

from flask import render_template, request, jsonify, session, redirect, url_for, flash
from datetime import datetime
from models import HouseStatusModel, RepairRequestModel, AppointmentModel, HouseInfoModel, HouseListingAuditModel, db

def house_statistics_logic():
    if session.get('user_type') != 2:
        flash('无权访问', 'error')
        return redirect(url_for('account.landlord_home'))
    landlord_name = session.get('username')
    total_houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name).count()
    available_houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name, status=0).count()
    rented_houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name, status=1).count()
    unlisted_houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name, status=2).count()
    pending_houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name, status=4).count()
    recent_repairs = RepairRequestModel.query.filter_by(
        landlord_username=landlord_name,
        status='请求中'
    ).count()
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
    return render_template('house/statictis.html', stats=stats)

def batch_house_action_logic():
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
                house_status.status = 4
                house_status.update_time = datetime.now()
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

