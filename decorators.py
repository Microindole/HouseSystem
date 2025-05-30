from functools import wraps
from flask import session, redirect, url_for, request, make_response, flash, g
import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'your_secret_key'  # 请与account.py保持一致


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except Exception:
        return None


# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'username' not in session:
#             # 判断是否为异步请求（通用：只要是前端脚本请求都可拦截）
#             is_script_request = (
#                 request.headers.get('X-Requested-With') == 'XMLHttpRequest' or
#                 request.accept_mimetypes.best == 'application/json' or
#                 request.is_json
#             )
#             if is_script_request:
#                 resp = make_response('NEED_LOGIN', 401)
#                 resp.headers['X-Need-Login'] = '1'
#                 return resp
#             # 非脚本请求，弹窗提示并跳转
#             html = """
#             <script>
#                 alert('请先登录！');
#                 window.location.href = '{}';
#             </script>
#             """.format(url_for('account.login'))
#             return html
#         return f(*args, **kwargs)
#     return decorated_function


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('access_token')
        payload = verify_token(token) if token else None
        if not payload:
            flash('请先登录！', 'warning')
            return redirect(url_for('account.login'))
        if payload.get('user_type') == 0:
            g.username = payload.get('username')
            g.user_type = payload.get('user_type')
            return func(*args, **kwargs)
        else:
            flash('您没有权限访问此页面。', 'danger')
            return redirect(url_for('index'))
    return wrapper


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')
        payload = verify_token(token) if token else None
        if not payload:
            # 判断是否为异步请求（通用：只要是前端脚本请求都可拦截）
            is_script_request = (
                request.headers.get('X-Requested-With') == 'XMLHttpRequest' or
                request.accept_mimetypes.best == 'application/json' or
                request.is_json
            )
            if is_script_request:
                resp = make_response('NEED_LOGIN', 401)
                resp.headers['X-Need-Login'] = '1'
                return resp
            # 非脚本请求，弹窗提示并跳转
            html = """
            <script>
                alert('请先登录！');
                window.location.href = '{}';
            </script>
            """.format(url_for('account.login'))
            return html
        g.username = payload['username']
        g.user_type = payload['user_type']
        return f(*args, **kwargs)
    return decorated
