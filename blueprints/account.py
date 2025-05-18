from datetime import datetime

from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session, flash # 确保导入 flash
from sqlalchemy import func, cast, Date
from sqlalchemy.orm import joinedload

from models import LoginModel, db, TenantModel, LandlordModel, HouseStatusModel, DailyRentRateModel, \
    HouseListingAuditModel, HouseInfoModel
from models import LoginModel, TenantModel, LandlordModel, EmailUsernameMapModel # 新增导入 EmailUsernameMapModel
from blueprints.forms import LoginForm, RegisterForm
from decorators import login_required
from argon2 import PasswordHasher, exceptions as argon2_exceptions
from flask_mail import Message
from exts import mail, db
import string
import random
from flask import current_app

ph = PasswordHasher()


def generate_code(length=6):
    """生成随机数字验证码"""
    return ''.join(random.choices(string.digits, k=length))

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

            # 使用argon2校验密码
            try:
                ph.verify(user_login.password, password)
            except argon2_exceptions.VerifyMismatchError:
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
        form = LoginForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data

            admin_user = LoginModel.query.filter_by(username=username, type=0).first()
            if not admin_user:
                flash('管理员用户名或密码错误，或非管理员账户。', 'error')
                return render_template('account/admin_login.html', form=form)
            try:
                ph.verify(admin_user.password, password)
            except argon2_exceptions.VerifyMismatchError:
                flash('管理员用户名或密码错误，或非管理员账户。', 'error')
                return render_template('account/admin_login.html', form=form)

            session['username'] = admin_user.username
            session['user_type'] = admin_user.type
            return redirect(url_for('account.admin_dashboard'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{form[field].label.text}: {error}", "error")
            return render_template('account/admin_login.html', form=form)


@account_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("account/register.html")
    else:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        user_type_str = request.form.get('user_type', '')
        email_code = request.form.get('email_code', '').strip()

        errors = []
        if not username or len(username) < 3 or len(username) > 20 or not username.isalnum() and '_' not in username:
             errors.append("用户名格式不正确或长度不符合要求。")
        else:
            temp_form = RegisterForm()
            username_error = temp_form.validate_username_on_server(username)
            if username_error:
                errors.append(username_error)

        if not password or len(password) < 6 or len(password) > 20:
            errors.append("密码长度必须在6到20个字符之间。")

        if not email or '@' not in email or '.' not in email.split('@')[-1]: # Basic server check
            errors.append("请输入有效的邮箱地址。")

        if not phone or not (phone.isdigit() and len(phone) == 11):
            errors.append("请输入11位有效手机号。")

        if not address: # Address is combined by JS, check if it's present
            errors.append("地址不能为空，请选择省市区。")

        user_type = None
        if user_type_str in ['1', '2']:
            user_type = int(user_type_str)
        else:
            errors.append("请选择有效的用户角色。")

        # 校验邮箱验证码
        real_code = session.get('email_code')
        real_email = session.get('email_code_email')
        if not real_code or not real_email or email_code != real_code or email != real_email:
            errors.append("邮箱验证码错误或已过期，请重新获取。")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("account/register.html", submitted_data=request.form)
        hashed_password = ph.hash(password)
        new_user_login = LoginModel(username=username, password=hashed_password, type=user_type)
        db.session.add(new_user_login)

        if user_type == 1:
            new_tenant = TenantModel(tenant_name=username, phone=phone, addr=address)
            db.session.add(new_tenant)
        elif user_type == 2:
            new_landlord = LandlordModel(landlord_name=username, phone=phone, addr=address)
            db.session.add(new_landlord)
        try:
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            flash(f"注册时发生内部错误 (flush阶段): {str(e)}", "error")
            return render_template("account/register.html", submitted_data=request.form)
        new_email_map = EmailUsernameMapModel(email=email, username=username)
        db.session.add(new_email_map)

        try:
            db.session.commit()
            flash("注册成功！现在可以登录了。", "success")
            return redirect(url_for('account.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"注册失败，发生数据库错误: {str(e)}", "error")
            return render_template("account/register.html", submitted_data=request.form)


@account_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """个人信息修改页面"""
    if 'username' not in session:
        return redirect(url_for('account.login'))
    username = session['username']
    user_type = session.get('user_type')
    user_email_obj = EmailUsernameMapModel.query.filter_by(username=username).first()
    user_email = user_email_obj.email if user_email_obj else "未绑定邮箱"

    if request.method == 'GET':
        # 加载用户信息
        user = None
        if user_type == 1:
            user = TenantModel.query.filter_by(tenant_name=username).first()
        elif user_type == 2:
            user = LandlordModel.query.filter_by(landlord_name=username).first()
        elif user_type == 0:
            user = LoginModel.query.filter_by(username=username).first()
        return render_template('account/profile.html', user=user, user_type=user_type, user_email=user_email)

    elif request.method == 'POST':
        # 获取表单数据
        new_username = request.form.get('username')
        phone = request.form.get('phone')
        password = request.form.get('password')
        verification_code = request.form.get('verification_code')
        address = None

        # 校验验证码
        real_code = session.get('email_code')
        real_email = session.get('email_code_email')
        if not real_code or not real_email or verification_code != real_code:
            flash("验证码错误或已过期，请重新获取。", "profile_error")
            return redirect(url_for('account.profile'))

        # 验证通过后清除验证码
        session.pop('email_code', None)
        session.pop('email_code_email', None)

        if user_type in [1, 2]:
            province = request.form.get('province')
            city = request.form.get('city')
            district = request.form.get('district')
            if province and city and district:
                address = f"{province}{city}{district}"

        try:
            # 修改用户信息逻辑（保持原有逻辑）
            if user_type == 1:
                user_to_update = TenantModel.query.filter_by(tenant_name=username).first()
                if user_to_update:
                    if address:
                        user_to_update.addr = address
                    user_to_update.phone = phone
                    if new_username != username:
                        if LoginModel.query.filter_by(username=new_username).first():
                            flash(f"用户名 '{new_username}' 已被占用。", "profile_error")
                            return redirect(url_for('account.profile'))
                        user_to_update.tenant_name = new_username

            elif user_type == 2:
                user_to_update = LandlordModel.query.filter_by(landlord_name=username).first()
                if user_to_update:
                    if address:
                        user_to_update.addr = address
                    user_to_update.phone = phone
                    if new_username != username:
                        if LoginModel.query.filter_by(username=new_username).first():
                            flash(f"用户名 '{new_username}' 已被占用。", "profile_error")
                            return redirect(url_for('account.profile'))
                        user_to_update.landlord_name = new_username

            elif user_type == 0:
                user_to_update = LoginModel.query.filter_by(username=username).first()
                if new_username != username:
                    if LoginModel.query.filter_by(username=new_username).first():
                        flash(f"用户名 '{new_username}' 已被占用。", "profile_error")
                        return redirect(url_for('account.profile'))
                user_to_update.username = new_username

            login_user = LoginModel.query.filter_by(username=username).first()
            if login_user:
                if new_username != username:
                    login_user.username = new_username
                if password:
                    login_user.password = ph.hash(password)

            db.session.commit()
            flash("用户信息修改成功！", "profile")
            return redirect(url_for('account.profile'))

        except Exception as e:
            db.session.rollback()
            flash(f"用户信息修改失败：{str(e)}", "profile_error")
            return redirect(url_for('account.profile'))


@account_bp.route('/send_email_code', methods=['POST'])
def send_email_code():
    email = request.form.get('email')
    if not email or '@' not in email:
        return jsonify({'success': False, 'msg': '请输入有效邮箱'}), 400

    code = generate_code()
    # 用 session 存储验证码和邮箱
    session['email_code'] = code
    session['email_code_email'] = email

    try:
        msg = Message("智能房屋租赁系统验证码",
                      recipients=[email],
                      body=f"您的验证码是：{code}，5分钟内有效。")
        mail.send(msg)
        return jsonify({'success': True, 'msg': '验证码已发送'})
    except Exception as e:
        current_app.logger.error(f"邮件发送失败: {e}")
        return jsonify({'success': False, 'msg': '邮件发送失败，请稍后重试'}), 500


from flask import request, jsonify, session
from flask_mail import Message
import time

# 发送重置验证码
@account_bp.route('/send_reset_code', methods=['POST'])
def send_reset_code():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    # 校验用户名和邮箱是否匹配
    user = LoginModel.query.filter_by(username=username).first()
    email_map = EmailUsernameMapModel.query.filter_by(username=username, email=email).first()
    if not user or not email_map:
        return jsonify({'success': False, 'msg': '用户名和邮箱不匹配'})
    # 生成验证码
    code = generate_code()
    session['reset_code'] = code
    session['reset_code_email'] = email
    session['reset_code_username'] = username
    session['reset_code_time'] = int(time.time())
    try:
        msg = Message("重置密码验证码", recipients=[email], body=f"您的验证码是：{code}，5分钟内有效。")
        mail.send(msg)
        return jsonify({'success': True, 'msg': '验证码已发送，请查收邮箱'})
    except Exception as e:
        current_app.logger.error(f"重置密码邮件发送失败: {e}")
        return jsonify({'success': False, 'msg': '邮件发送失败，请稍后重试'})

# 校验验证码
@account_bp.route('/verify_reset_code', methods=['POST'])
def verify_reset_code():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    code = data.get('code', '').strip()
    real_code = session.get('reset_code')
    real_email = session.get('reset_code_email')
    real_username = session.get('reset_code_username')
    code_time = session.get('reset_code_time')
    if not real_code or not real_email or not real_username or not code_time:
        return jsonify({'success': False, 'msg': '请先获取验证码'})
    if int(time.time()) - code_time > 300:
        return jsonify({'success': False, 'msg': '验证码已过期'})
    if code != real_code or email != real_email or username != real_username:
        return jsonify({'success': False, 'msg': '验证码错误'})
    return jsonify({'success': True, 'msg': '验证通过'})

# 重置密码
@account_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    code = data.get('code', '').strip()
    password = data.get('password', '').strip()
    real_code = session.get('reset_code')
    real_email = session.get('reset_code_email')
    real_username = session.get('reset_code_username')
    code_time = session.get('reset_code_time')
    if not real_code or not real_email or not real_username or not code_time:
        return jsonify({'success': False, 'msg': '请先获取验证码'})
    if int(time.time()) - code_time > 300:
        return jsonify({'success': False, 'msg': '验证码已过期'})
    if code != real_code or email != real_email or username != real_username:
        return jsonify({'success': False, 'msg': '验证码错误'})
    # 修改密码
    user = LoginModel.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'msg': '用户不存在'})
    user.password = ph.hash(password)
    db.session.commit()
    # 清除验证码
    session.pop('reset_code', None)
    session.pop('reset_code_email', None)
    session.pop('reset_code_username', None)
    session.pop('reset_code_time', None)
    return jsonify({'success': True, 'msg': '密码重置成功，请重新登录'})


@account_bp.route('/logout', methods=['GET', 'POST'])
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

    landlord_name = session.get('username')
    houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name).all()
    for house in houses:
        house.latest_audit = HouseListingAuditModel.query.filter_by(house_id=house.house_id).order_by(
            HouseListingAuditModel.id.desc()).first()
    return render_template('landlord_home.html',houses=houses)






@account_bp.route('/admin/dashboard')
@login_required # 并且应该有 admin_required 装饰器
# @admin_required # 假设您已经定义了这个装饰器
def admin_dashboard():
    """管理员后台"""
    if session.get('user_type') != 0: # 再次确认是管理员
        flash("无权访问管理员后台。", "danger")
        return redirect(url_for('account.login')) # 或者首页
    return render_template('admin_dashboard.html')



@account_bp.route('/admin/users', methods=['GET', 'POST'])
def manage_users():
    if session.get('user_type') != 0:
        return redirect(url_for('account.login'))

    # 获取所有用户（根据你的模型调整）
    tenants = TenantModel.query.all()
    landlords = LandlordModel.query.all()
    admins = LoginModel.query.filter_by(type=3).all()

    return render_template('management/manage_users.html', tenants=tenants, landlords=landlords, admins=admins)


@account_bp.route('/admin/reset_userpassword', methods=['POST'])
def reset_userpassword():
    if session.get('user_type') != 0:
        return redirect(url_for('account.login'))

    username = request.form.get('username')
    login_user = LoginModel.query.filter_by(username=username).first()
    if login_user:
        password = '123456'
        hashed_password = ph.hash(password)
        login_user.password=hashed_password
        db.session.commit()
    return redirect(url_for('account.manage_users'))

@account_bp.route('/admin/landlord_houses/<landlord_name>')
def get_landlord_houses(landlord_name):
    if session.get('user_type') != 0:
        return redirect(url_for('account.login'))

    houses = HouseStatusModel.query.options(
        joinedload(HouseStatusModel.house_info)
    ).filter_by(landlord_name=landlord_name).all()

    house_list = []
    for h in houses:
        house_info = h.house_info  # 通过关系获取 HouseInfoModel 实例
        house_list.append({
            'house_id': h.house_id,
            'status': h.status,
            'phone': h.phone,
            'update_time': h.update_time.strftime('%Y-%m-%d %H:%M'),
            'house_name': house_info.house_name if house_info else '',
            'region': house_info.region if house_info else '',
            'addr': house_info.addr if house_info else ''
        })

    return jsonify(house_list)
@account_bp.route('/admin/down_house', methods=['POST'])
def down_house():
    if session.get('user_type') != 0:
        return jsonify({'success': False, 'message': '权限不足'}), 403

    house_id = request.json.get('house_id')
    landlord_name = request.json.get('landlord_name')

    house = HouseStatusModel.query.filter_by(house_id=house_id, landlord_name=landlord_name).first()
    if house and house.status == 0:
        house.status = 2
        house.update_time = datetime.now()
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': '房源不存在或无法下架'}), 400


@account_bp.route('/api/rent_rate_history', methods=['GET'])
def rent_rate_history():
    # 获取请求中的日期参数
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({'error': '缺少开始日期或结束日期'}), 400

    # 将字符串转换为日期对象
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # 查询指定日期范围内的出租率数据
    records = db.session.query(DailyRentRateModel).filter(
        DailyRentRateModel.date.between(start_date, end_date)
    ).all()

    # 格式化返回的数据
    dates = [record.date.strftime('%Y-%m-%d') for record in records]
    rates = [round(record.rent_rate, 2) for record in records]

    return jsonify({
        'dates': dates,
        'rates': rates
    })
#跳转系统设置页面
@account_bp.route('/admin/system_setting')
def system_setting():
    if session.get('user_type') != 0:
        return redirect(url_for('account.login'))
    return render_template('management/manage_statistic.html')


@account_bp.route('/admin/manual_rent_rate_update')
def manual_rent_rate_update():
    today = datetime.today().date()
    total = HouseStatusModel.query.filter(HouseStatusModel.status.in_([0, 1])).count()
    rented = HouseStatusModel.query.filter_by(status=1).count()

    rent_rate = round((rented / total) * 100, 2) if total > 0 else 0

    existing_record = DailyRentRateModel.query.filter_by(date=today).first()
    if existing_record:
        existing_record.total_count = total
        existing_record.rented_count = rented
        existing_record.rent_rate = rent_rate
        message = "已更新今日出租率记录"
    else:
        new_record = DailyRentRateModel(
            date=today,
            total_count=total,
            rented_count=rented,
            rent_rate=rent_rate
        )
        db.session.add(new_record)
        message = "已添加今日出租率记录"

    db.session.commit()

    return jsonify({
        "message": message,
        "date": str(today),
        "total": total,
        "rented": rented,
        "rent_rate": rent_rate
    })


@account_bp.route('/account/admin/audit_list')
def audit_list():
    audits = HouseListingAuditModel.query.all()

    # 自定义排序：
    # 审核中放前面（audit_status == 0），其他按 update_time 倒序
    audits.sort(key=lambda a: (a.audit_status != 0, -a.update_time.timestamp() if a.update_time else 0))

    return render_template('management/manage_audit.html', audits=audits)

@account_bp.route('/account/admin/audit/approve/<int:audit_id>')
def approve_audit(audit_id):
    audit = HouseListingAuditModel.query.get(audit_id)
    if audit and audit.audit_status == 0:
        # 1. 更新审核记录状态为已通过
        audit.audit_status = 1
        audit.update_time = datetime.utcnow()

        # 2. 同步修改房源状态（比如将其设置为上架状态）
        house = HouseStatusModel.query.filter_by(house_id=audit.house_id).first()
        if house:
            house.status = 0  # 上架

        db.session.commit()
    return redirect(url_for('account.audit_list'))

@account_bp.route('/admin/audit/reject_ajax', methods=['POST'])
def reject_audit_ajax():
    data = request.get_json()
    audit_id = data.get('audit_id')
    reason = data.get('reason')

    audit = HouseListingAuditModel.query.get(audit_id)
    if audit and audit.audit_status == 0:
        audit.audit_status = 2  # 设置为“已拒绝”
        audit.reason = reason
        audit.update_time = datetime.utcnow()

        # 可选：同步修改房源状态为“审核未通过”或“冻结”
        house = HouseStatusModel.query.filter_by(house_id=audit.house_id).first()
        if house:
            house.status = 5

        db.session.commit()
        return jsonify({'code': 200, 'msg': '拒绝成功'})
    else:
        return jsonify({'code': 400, 'msg': '该记录不存在或已被处理'}), 400


@account_bp.route('/landlord/submit_listing', methods=['POST'])
def submit_listing():
    house_id = request.form.get('house_id')
    landlord_name = session.get('username')

    # 确保拿到的是联合主键的数据
    house_status = HouseStatusModel.query.filter_by(
        house_id=house_id,
        landlord_name=landlord_name
    ).first()

    if not house_status:
        return '房源不存在或无权限操作', 404

    if house_status.status != 2 and house_status.status != 5:
        return '当前状态不能提交申请', 400

    # 更新状态为 4：待审核
    house_status.status = 4

    # 同时新增审核记录
    audit = HouseListingAuditModel(
        house_id=house_status.house_id,
        house_name=house_status.house_info.house_name,
        landlord_name=house_status.landlord_name,
        audit_status=0,  # 0 表示审核中
        reason=None,
    )

    db.session.add(audit)
    db.session.commit()
    return redirect(url_for('account.landlord_home'))