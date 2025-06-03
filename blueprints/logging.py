from flask import Blueprint, request, jsonify
from models import db, OperationLog
from datetime import datetime

logging_bp = Blueprint('logging', __name__)
USER_TYPE_MAP = {
    0: '管理员',
    1: '租客',
    2: '房东'
}

@logging_bp.route('/api/logs', methods=['GET'])
def get_logs():
    limit = request.args.get('limit', type=int)
    search = request.args.get('search', '', type=str)

    query = OperationLog.query.order_by(OperationLog.created_at.desc())

    if search:
        keyword = f"%{search}%"
        query = query.filter(
            (OperationLog.username.like(keyword)) |
            (OperationLog.message.like(keyword))
        )

    logs = query.limit(limit).all() if limit else query.all()

    log_list = []
    for log in logs:
        log_list.append({
            'username': log.username,
            'user_type': USER_TYPE_MAP.get(log.user_type, '未知'),
            'message': log.message,
            'timestamp': log.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify({'logs': log_list})