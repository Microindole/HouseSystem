from functools import wraps
from flask import session, redirect, url_for, request, make_response, flash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
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
        return f(*args, **kwargs)
    return decorated_function


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 首先检查是否已登录
        if not session.get('username'):
            flash('请先登录！', 'warning')
            return redirect(url_for('login.login_page')) # 调整为您的登录路由
        # 然后检查用户类型是否为管理员 (假设管理员的 user_type 为 0)
        if session.get('user_type') == 0:
            return func(*args, **kwargs)
        else:
            flash('您没有权限访问此页面。', 'danger')
            # 可以重定向到首页或其他无权限提示页面
            return redirect(url_for('index')) # 假设您的首页路由名为 'index'
    return wrapper
