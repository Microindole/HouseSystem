import json
import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, abort, flash, current_app, g
from sqlalchemy import or_
from datetime import datetime
from models import (HouseInfoModel, HouseStatusModel, CommentModel, NewsModel,
                   TenantModel, LandlordModel, AppointmentModel, RepairRequestModel, db, HouseListingAuditModel)
from decorators import login_required

# 导入各功能模块的 service 方法
from service.house_service import (
    allowed_file,
    get_cities_data,
    get_house_list,
    get_house_detail,
    add_house_logic,
    edit_house_logic,
    delete_house_logic,
    update_house_status_logic,
    export_houses_csv,
    api_house_search_logic
)
from service.news_service import (
    add_news_logic,
    manage_news_logic,
    delete_news_logic,
    batch_delete_news_logic,
    load_more_news_logic,
    news_detail_logic,  # 新增
    news_list_logic     # 新增
)
from service.repair_service import (
    create_repair_request_logic,
    manage_repair_requests_logic,
    handle_repair_request_logic
)
from service.comment_service import add_comment_form_logic
from service.appointment_service import (
    create_appointment_logic,
    view_appointments_logic,
    update_appointment_status_logic
)
from service.statistics_service import (
    house_statistics_logic,
    batch_house_action_logic
)

house_bp = Blueprint('house', __name__)

@house_bp.route('', methods=['GET'])
def house_list():
    return get_house_list()

@house_bp.route('/<int:house_id>', methods=['GET'])
def house_detail(house_id):
    return get_house_detail(house_id)

@house_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_house():
    return add_house_logic()

@house_bp.route('/edit/<int:house_id>', methods=['GET', 'POST'])
@login_required
def edit_house(house_id):
    return edit_house_logic(house_id)

@house_bp.route('/delete/<int:house_id>', methods=['POST'])
@login_required
def delete_house(house_id):
    return delete_house_logic(house_id)

@house_bp.route('/batch/action', methods=['POST'])
@login_required
def batch_house_action():
    return batch_house_action_logic()

@house_bp.route('/news/add', methods=['GET', 'POST'])
@login_required
def add_news():
    return add_news_logic()

@house_bp.route('/news/manage')
@login_required
def manage_news():
    return manage_news_logic()

@house_bp.route('/news/delete/<int:news_id>', methods=['POST'])
@login_required
def delete_news(news_id):
    return delete_news_logic(news_id)

@house_bp.route('/news/batch-delete', methods=['POST'])
@login_required
def batch_delete_news():
    return batch_delete_news_logic()

@house_bp.route('/repair/request', methods=['POST'])
@login_required
def create_repair_request():
    return create_repair_request_logic()

@house_bp.route('/repair/manage')
@login_required
def manage_repair_requests():
    return manage_repair_requests_logic()

@house_bp.route('/repair/handle/<int:request_id>', methods=['POST'])
@login_required
def handle_repair_request(request_id):
    return handle_repair_request_logic(request_id)

@house_bp.route('/add_comment_form', methods=['POST'])
@login_required
def add_comment_form():
    return add_comment_form_logic()

@house_bp.route('/appointment', methods=['POST'])
@login_required
def create_appointment():
    return create_appointment_logic()

@house_bp.route('/appointments', methods=['GET'])
@login_required
def view_appointments():
    return view_appointments_logic()

@house_bp.route('/appointment/<int:appointment_id>/update', methods=['POST'])
@login_required
def update_appointment_status(appointment_id):
    return update_appointment_status_logic(appointment_id)

@house_bp.route('/status/update/<int:house_id>', methods=['POST'])
@login_required
def update_house_status(house_id):
    return update_house_status_logic(house_id)

@house_bp.route('/statistics')
@login_required
def house_statistics():
    return house_statistics_logic()

@house_bp.route('/api/search', methods=['GET'])
def api_house_search():
    return api_house_search_logic()

@house_bp.route('/export')
@login_required
def export_houses():
    landlord_name = g.username
    return export_houses_csv(landlord_name)


@house_bp.route('/load_more_news', methods=['GET'])
def load_more_news():
    return load_more_news_logic()

# 新增新闻详情路由
@house_bp.route('/news/<int:news_id>')
def news_detail(news_id):
    return news_detail_logic(news_id)

# 新增新闻列表路由
@house_bp.route('/news')
def news_list():
    return news_list_logic()
