from flask import g, request
from models import db, OperationLog

def log_login(username, user_type, message="登录系统"):
    log = OperationLog(
        username=username,
        user_type=user_type,
        message=message,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

def log_operation(username, user_type, message):
    log = OperationLog(
        username=username,
        user_type=user_type,
        message=message,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

