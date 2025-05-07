from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session, flash # 确保导入 flash
from models import LoginModel, db, TenantModel, LandlordModel
from blueprints.forms import LoginForm, RegisterForm
from decorators import login_required

# 后面模版引擎的重定向account.login的account就是来自这里
account_bp = Blueprint("account", __name__, url_prefix="/account") # 建议为蓝图添加 url_prefix


@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("account/login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            role = request.form.get('role')

            user_login = LoginModel.query.filter_by(username=username).first()

            if not user_login:
                flash("用户名不存在！", "error")
                return render_template("account/login.html", form=form)

            if user_login.password != password: # 注意：实际项目中应使用哈希密码比较
                flash("密码错误！", "error")
                return render_template("account/login.html", form=form)

            # 将角色映射为数值并验证
            expected_user_type = None
            redirect_url = None

            if role == 'tenant':
                expected_user_type = 1
                # 验证 TenantModel 中是否存在该用户（可选，但更严谨）
                tenant_exists = TenantModel.query.filter_by(tenant_name=username).first()
                if not tenant_exists:
                    flash("租客信息不存在或角色选择错误。", "error")
                    return render_template("account/login.html", form=form)
                redirect_url = url_for('account.tenant_home')
            elif role == 'landlord':
                expected_user_type = 2
                # 验证 LandlordModel 中是否存在该用户（可选，但更严谨）
                landlord_exists = LandlordModel.query.filter_by(landlord_name=username).first()
                if not landlord_exists:
                    flash("房东信息不存在或角色选择错误。", "error")
                    return render_template("account/login.html", form=form)
                redirect_url = url_for('account.landlord_home')
            else:
                flash("无效的用户角色，请重新选择。", "error")
                return render_template("account/login.html", form=form)

            if user_login.type != expected_user_type:
                flash("角色与用户名不匹配，请重新输入。", "error")
                return render_template("account/login.html", form=form)

            session['username'] = username
            session['user_type'] = user_login.type # 使用从数据库查询到的类型
            return redirect(redirect_url)
        else:
            # 将表单验证错误传递给模板
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{form[field].label.text}: {error}", "error")
            return render_template("account/login.html", form=form)


# --- 新增管理员登录路由 ---
@account_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('account/admin_login.html')
    else:
        # 可以复用 LoginForm，或者为管理员创建一个特定的表单
        form = LoginForm(request.form) # 假设管理员登录也只需要用户名和密码
        if form.validate():
            username = form.username.data
            password = form.password.data

            admin_user = LoginModel.query.filter_by(username=username, type=0).first() # 假设管理员 type 为 0

            if admin_user and admin_user.password == password: # 实际应使用哈希密码比较
                session['username'] = admin_user.username
                session['user_type'] = admin_user.type # 应该是 0
                # flash('管理员登录成功！', 'success') # 可选的成功提示
                return redirect(url_for('account.admin_dashboard')) # 或者其他管理员后台首页
            else:
                flash('管理员用户名或密码错误，或非管理员账户。', 'error')
                return render_template('account/admin_login.html', form=form)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{form[field].label.text}: {error}", "error")
            return render_template('account/admin_login.html', form=form)


@account_bp.route('/register', methods=['GET', 'POST'])
def register():
    # ... (您的注册逻辑) ...
    # 注意：注册逻辑不应该允许用户直接注册为管理员 (type=0)
    # 管理员账户通常由系统初始化或通过特定管理接口创建
    if request.method == "GET":
        return render_template("account/register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            phone = form.phone.data  # 获取联系方式
            address = form.address.data  # 获取地址信息
            user_type = int(form.user_type.data)  # 获取角色选择并转换为整数

            # 检查用户名是否已存在
            existing_user = LoginModel.query.filter_by(username=username).first()
            if existing_user:
                error="用户名已存在!"
                return render_template("account/register.html", error="用户名已存在！")

            # 创建新用户并保存到 login 表
            new_user = LoginModel(username=username, password=password, type=user_type)
            db.session.add(new_user)

            # 根据角色类型保存到 tenant 或 landlord 表
            if user_type == 1:  # 租客
                new_tenant = TenantModel(tenant_name=username, phone=phone, addr=address)
                db.session.add(new_tenant)
            elif user_type == 2:  # 房东
                new_landlord = LandlordModel(landlord_name=username, phone=phone, addr=address)
                db.session.add(new_landlord)

            # 提交所有更改
            db.session.commit()

            print("注册成功！")
            return redirect(url_for('account.login'))
        else:
            print(form.errors)
            return render_template("account/register.html", errors=form.errors)


@account_bp.route('/profile', methods=['GET', 'POST'])
@login_required # 确保个人信息页面需要登录
def profile():
    """个人信息修改页面"""
    if 'username' not in session:
        # 如果用户未登录，重定向到登录页面
        return redirect(url_for('account.login'))

    username = session['username']
    user_type = session.get('user_type')
    #GEI和POST分别代表跳转该页面和点击按钮所执行的代码
    if request.method == 'GET':
        # 根据用户角色加载对应的个人信息
        if user_type == 1:  # 租客
            user = TenantModel.query.filter_by(tenant_name=username).first()
        elif user_type == 2:  # 房东
            user = LandlordModel.query.filter_by(landlord_name=username).first()
        else:  # 管理员
            user = LoginModel.query.filter_by(username=username).first()

        return render_template('account/profile.html', user=user, user_type=user_type)

    elif request.method == 'POST':
        # 获取表单数据
        new_username = request.form.get('username')  # 新用户名
        phone = request.form.get('phone')  # 联系方式
        province = request.form.get('province')  # 省份
        city = request.form.get('city')  # 城市
        district = request.form.get('district')  # 区县
        password = request.form.get('password')  # 新密码

        address = f"{province}{city}{district}"
        try:
            # 根据用户角色更新对应的表
            if user_type == 1:  # 租客
                user = TenantModel.query.filter_by(tenant_name=username).first()
                if user:
                    user.tenant_name = new_username  # 更新用户名
                    user.phone = phone
                    user.addr = address
                    # 同时更新 login 表中的用户名和密码
                    login_user = LoginModel.query.filter_by(username=username).first()
                    if login_user:
                        login_user.username = new_username
                        if password:
                            login_user.password = password

            elif user_type == 2:  # 房东
                user = LandlordModel.query.filter_by(landlord_name=username).first()
                if user:
                    user.landlord_name = new_username  # 更新用户名
                    user.phone = phone
                    user.addr = address
                    # 同时更新 login 表中的用户名和密码
                    login_user = LoginModel.query.filter_by(username=username).first()
                    if login_user:
                        login_user.username = new_username
                        if password:
                            login_user.password = password

            else:  # 管理员
                user = LoginModel.query.filter_by(username=username).first()
                if user:
                    user.username = new_username  # 更新用户名
                    user.phone = phone
                    if password:
                        user.password = password

            # 提交更改到数据库
            db.session.commit()

            # 更新 session 中的用户名
            session['username'] = new_username
            return render_template('account/profile.html', success="用户信息修改成功！", user=user, user_type=user_type)

        except Exception as e:
            db.session.rollback()
            return render_template('account/profile.html', error=f"用户信息修改失败：{str(e)}", user=user, user_type=user_type)


@account_bp.route('/logout',methods=['GET','POST'])
@login_required # 登出也应该是在登录状态下操作
def logout():
    """登出功能"""
    session.clear()
    flash("您已成功登出。", "info")
    return redirect(url_for('account.login'))


@account_bp.route('/tenant/home')
@login_required
def tenant_home():
    """租客首页"""
    if session.get('user_type') != 1:
        flash("无权访问。", "warning")
        return redirect(url_for('index')) # 或者合适的错误页面/首页
    return render_template('tenant_home.html')


@account_bp.route('/landlord/home')
@login_required
def landlord_home():
    """房东首页"""
    if session.get('user_type') != 2:
        flash("无权访问。", "warning")
        return redirect(url_for('index')) # 或者合适的错误页面/首页
    return render_template('landlord_home.html')


@account_bp.route('/admin/dashboard')
@login_required # 并且应该有 admin_required 装饰器
# @admin_required # 假设您已经定义了这个装饰器
def admin_dashboard():
    """管理员后台"""
    if session.get('user_type') != 0: # 再次确认是管理员
        flash("无权访问管理员后台。", "danger")
        return redirect(url_for('account.login')) # 或者首页
    return render_template('admin_dashboard.html')
