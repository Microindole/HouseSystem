from flask import render_template, request, jsonify, Blueprint, redirect, url_for, session, flash
from blueprints.pay import alipay_obj, ALIPAY_SETTING
from decorators import login_required # 导入 login_required 装饰器
import time 
import random

pay_bp = Blueprint('pay', __name__)

@pay_bp.route('/good_list', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@pay_bp.route('/pay', methods=['GET', 'POST'])
@login_required # 添加登录保护
def good_list_view():
    if request.method == 'GET':
        return render_template('paytest.html')
    # 如果是post，我们认为是购买
    alipay = alipay_obj()
    
    # 生成唯一的订单号
    # 方法1: 时间戳（到秒）+ 4位随机数
    # current_time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # random_suffix = "".join(random.sample("0123456789", 4))
    # unique_out_trade_no = f"{current_time_str}{random_suffix}"

    # 方法2: 更精确的时间戳（到毫秒）
    unique_out_trade_no = str(int(time.time() * 1000)) + str(random.randint(1000,9999))


    # 生成支付路由
    # 拼接url--返回url
    # 电脑网站支付，需要跳转到：https://openapi-sandbox.dl.alipaydev.com/gateway.do + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        # 这个订单号根据具体的商品名称进行修改，注意，路由可能要相应修改，这里是用时间戳生成随机订单号
        out_trade_no=unique_out_trade_no,  # 使用动态生成的唯一订单号

        # 注意，这里商品价格和商品名称也要实时修改

        total_amount=99999,  # 商品价格
        subject='999克拉的钻石',  # 商品的名称




        return_url=ALIPAY_SETTING.get('ALIPAY_RETURN_URL'),  # 同步回调网址--用于前端，付成功之后回调
        notify_url=ALIPAY_SETTING.get('ALIPAY_NOTIFY_URL')  # 异步回调网址---后端使用，post请求，网站未上线，post无法接收到响应内容
    )
    url = ALIPAY_SETTING.get('APIPAY_GATEWAY') + '?' + order_string
    return jsonify({'url': url, 'status': 1})

@pay_bp.route('/alipay/success_result/', methods=['POST', 'GET'])
@login_required # 添加登录保护
def alipay_success_result():
    # 支付宝同步回调，GET请求通常包含参数，POST通常是异步通知（但这里配置为同步）
    # 实际项目中，这里应该有验签逻辑来确认回调的合法性
    # data = request.args.to_dict() # GET请求的参数
    # signature = data.pop("sign")
    # success = alipay_obj().verify(data, signature)
    # if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
    #     print("支付成功，验签通过")
    # else:
    #     print("验签失败或支付未成功")
    #     flash("支付验证失败，请联系客服。", "error")
    #     return redirect(url_for('account.login')) # 或其他错误页面

    flash("支付成功！", "success")
    user_type = session.get('user_type')

    # 新增：租客支付成功后，修改合同和房屋状态
    if user_type == 1: # 租客
        from models import db, RentalContract, PrivateChannelModel, HouseStatusModel
        username = session.get('username')
        # 获取租客最新的待支付合同
        contract = RentalContract.query.filter_by(tenant_username=username, status=0).order_by(RentalContract.created_at.desc()).first()
        if contract:
            # 修改合同状态为已支付
            contract.status = 1
            # 找到对应房屋
            channel = PrivateChannelModel.query.get(contract.channel_id)
            if channel:
                house_status = HouseStatusModel.query.filter_by(house_id=channel.house_id, landlord_name=contract.landlord_username).first()
                if house_status:
                    house_status.status = 1  # 1为出租中
            db.session.commit()
        return redirect(url_for('account.tenant_home'))
    elif user_type == 2: # 房东
        # 理论上房东不直接支付，但按要求添加逻辑
        return redirect(url_for('account.landlord_home'))
    elif user_type == 0: # 管理员
        # 理论上管理员不直接支付
        return redirect(url_for('account.admin_dashboard'))
    else:
        # 未知用户类型或未登录（理论上 login_required 会处理未登录）
        flash("无法确定用户类型，将返回登录页面。", "warning")
        return redirect(url_for('account.login')) # 默认跳转到登录页



@pay_bp.route('/alipay/fail_result/', methods=['POST', 'GET'])
@login_required # 支付失败页面也建议登录保护
def alipay_fail_result():
    flash("支付失败或已取消。", "error")
    # 可以选择渲染一个通用的支付失败页面，或者也根据用户类型跳转
    user_type = session.get('user_type')
    if user_type == 1:
        return redirect(url_for('account.tenant_home')) # 例如，让租客返回其首页
    # 对于其他类型或通用情况，可以渲染一个特定的失败页面
    return render_template('pay_fail_result.html')


@pay_bp.route('/contract_pay', methods=['POST'])
@login_required
def start_contract_payment():
    contract_id = request.form.get('contract_id')
    if not contract_id:
        flash("无效的合同 ID", "error")
        return redirect(url_for('contract.view_contracts'))

    from models import RentalContract
    contract = RentalContract.query.get(contract_id)
    if not contract:
        flash("合同不存在", "error")
        return redirect(url_for('contract.view_contracts'))

    # 只能由租客发起自己的支付
    if contract.tenant_username != session.get('username'):
        flash("无权限操作该合同支付", "error")
        return redirect(url_for('contract.view_contracts'))

    # 合同状态必须为0
    if contract.status != 0:
        flash("该合同已支付或已撤销", "error")
        return redirect(url_for('contract.view_contracts'))

    alipay = alipay_obj()

    # 金额（转为字符串），可以根据你的合同字段
    total_amount = str(contract.total_amount)
    # subject = f"租房合同支付 - 合同ID {contract_id}"
    subject = f"租房合同支付 - {contract.house_name}（{contract.addr}）"

    out_trade_no = str(int(time.time() * 1000)) + str(random.randint(1000, 9999))

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=out_trade_no,
        total_amount=total_amount,
        subject=subject,
        return_url=ALIPAY_SETTING.get('ALIPAY_RETURN_URL'),
        notify_url=ALIPAY_SETTING.get('ALIPAY_NOTIFY_URL')
    )

    url = ALIPAY_SETTING.get('APIPAY_GATEWAY') + '?' + order_string
    return redirect(url)
