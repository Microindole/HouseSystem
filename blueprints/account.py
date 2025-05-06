

from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from models import LoginModel, db, TenantModel, LandlordModel
from blueprints.forms import LoginForm, RegisterForm
from decorators import login_required

# 后面模版引擎的重定向account.login的account就是来自这里
account_bp = Blueprint("account", __name__)


@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("account/login.html")  # 渲染登录页面
    else:
        form = LoginForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data

            # 查询用户是否存在
            user = LoginModel.query.filter_by(username=username).first()
            if not user:
                error = "用户名不存在！"
                return render_template("account/login.html", error=error)

            if user.password == password:
                session['username'] = username
                session['user_type'] = user.type
                # 根据用户角色跳转到对应页面
                if user.type == 1:  # 租客
                    return redirect(url_for('account.tenant_home'))
                elif user.type == 2:  # 房东
                    return redirect(url_for('account.landlord_home'))
                elif user.type == 0:  # 管理员
                    return redirect(url_for('account.admin_dashboard'))
            else:
                error = "密码错误！"
                return render_template("account/login.html", error=error)
        else:
            # 表单验证失败
            return render_template("account/login.html", errors=form.errors)


@account_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("account/register.html")  # 渲染注册页面
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
def logout():
    """登出功能"""
    session.clear()  # 清除 session
    return redirect(url_for('account.login'))  # 返回登录页面


@account_bp.route('/tenant/home')
def tenant_home():
    """租客首页"""
    return render_template('tenant_home.html')


@account_bp.route('/landlord/home')
def landlord_home():
    """房东首页"""
    return render_template('landlord_home.html')


@account_bp.route('/admin/dashboard')
def admin_dashboard():
    """管理员后台"""
    return render_template('admin_dashboard.html')
