from flask import render_template, request, jsonify, Blueprint, redirect, url_for, session, flash, g
from blueprints.pay import alipay_obj, ALIPAY_SETTING
from decorators import login_required
from models import RentalContract, PrivateChannelModel, HouseInfoModel # 新增导入
import time
import random

pay_bp = Blueprint('pay', __name__)

@pay_bp.route('/good_list', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# @pay_bp.route('/pay', methods=['GET', 'POST'])
# @login_required
# def good_list_view():
#     if request.method == 'GET':
#         return render_template('paytest.html')
#     # 如果是post，我们认为是购买
#     alipay = alipay_obj()
#
#     # 生成唯一的订单号
#     # 方法1: 时间戳（到秒）+ 4位随机数
#     # current_time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
#     # random_suffix = "".join(random.sample("0123456789", 4))
#     # unique_out_trade_no = f"{current_time_str}{random_suffix}"
#
#     # 方法2: 更精确的时间戳（到毫秒）
#     unique_out_trade_no = str(int(time.time() * 1000)) + str(random.randint(1000,9999))
#
#
#     # 生成支付路由
#     # 拼接url--返回url
#     # 电脑网站支付，需要跳转到：https://openapi-sandbox.dl.alipaydev.com/gateway.do + order_string
#     order_string = alipay.api_alipay_trade_page_pay(
#         # 这个订单号根据具体的商品名称进行修改，注意，路由可能要相应修改，这里是用时间戳生成随机订单号
#         out_trade_no=unique_out_trade_no,  # 使用动态生成的唯一订单号
#
#         # 注意，这里商品价格和商品名称也要实时修改
#
#         total_amount=99999,  # 商品价格
#         subject='999克拉的钻石',  # 商品的名称
#
#
#
#
#         return_url=ALIPAY_SETTING.get('ALIPAY_RETURN_URL'),  # 同步回调网址--用于前端，付成功之后回调
#         notify_url=ALIPAY_SETTING.get('ALIPAY_NOTIFY_URL')  # 异步回调网址---后端使用，post请求，网站未上线，post无法接收到响应内容
#     )
#     url = ALIPAY_SETTING.get('APIPAY_GATEWAY') + '?' + order_string
#     return jsonify({'url': url, 'status': 1})

@pay_bp.route('/alipay/success_result/', methods=['POST', 'GET'])
@login_required
def alipay_success_result():
    # 实际应用中，支付宝回调会传递订单号等参数
    # 这里我们假设能从回调参数中获取 out_trade_no
    # 对于GET请求的同步回调，参数在request.args中
    # 对于POST请求的异步回调，参数在request.form中
    # 支付宝通常会传递 out_trade_no, trade_no, total_amount 等

    out_trade_no = request.args.get('out_trade_no') # 示例：从GET参数获取
    if not out_trade_no and request.method == 'POST':
        out_trade_no = request.form.get('out_trade_no') # 示例：从POST参数获取

    if not out_trade_no:
        flash("支付回调参数错误，无法确认订单。", "error")
        return redirect(url_for('contract.view_contracts'))

    # 从session中恢复合同ID
    contract_id_key = f'payment_pending_{out_trade_no}'
    contract_id = session.pop(contract_id_key, None) # 获取并移除

    if not contract_id:
        flash(f"无法找到与订单号 {out_trade_no} 关联的合同信息，请联系客服。", "error")
        # 可能需要更复杂的逻辑来处理这种情况，比如查询数据库中是否有未完成支付的订单与此out_trade_no匹配
        return redirect(url_for('contract.view_contracts'))

    flash("支付成功！", "success")
    user_type = g.user_type

    if user_type == 1: # 租客
        from models import db, RentalContract, PrivateChannelModel, HouseStatusModel

        contract = RentalContract.query.get(contract_id)
        if contract:
            if contract.tenant_username == g.username and contract.status == 1: # 确保是当前用户且状态为“已签署待支付”
                # 修改合同状态为已支付/合同生效
                contract.status = 4 # 新的状态码
                # 找到对应房屋
                channel = PrivateChannelModel.query.get(contract.channel_id)
                if channel:
                    house_status = HouseStatusModel.query.filter_by(house_id=channel.house_id, landlord_name=contract.landlord_username).first()
                    if house_status:
                        house_status.status = 1  # 1为出租中
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    flash(f"更新合同状态时发生错误: {str(e)}", "error")
            elif contract.status == 4:
                flash("此合同已支付。", "info")
            else:
                flash(f"合同状态异常 (ID: {contract.id}, Status: {contract.status})，请联系管理员。", "warning")
        else:
            flash(f"找不到合同 (ID: {contract_id})。", "error")
        return redirect(url_for('account.tenant_home'))
    elif user_type == 2: # 房东
        return redirect(url_for('account.landlord_home'))
    elif user_type == 0: # 管理员
        return redirect(url_for('account.admin_dashboard'))
    else:
        flash("无法确定用户类型，将返回登录页面。", "warning")
        return redirect(url_for('account.login'))



@pay_bp.route('/alipay/fail_result/', methods=['POST', 'GET'])
@login_required
def alipay_fail_result():
    flash("支付失败或已取消。", "error")
    # 可以选择渲染一个通用的支付失败页面，或者也根据用户类型跳转
    user_type = g.user_type
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

    contract = RentalContract.query.get(contract_id)
    if not contract:
        flash("合同不存在", "error")
        return redirect(url_for('contract.view_contracts'))

    # 只能由租客发起自己的支付
    if contract.tenant_username != g.username:
        flash("无权限操作该合同支付", "error")
        return redirect(url_for('contract.view_contracts'))

    # 修改：合同状态必须为 1 (已签署待支付) 才能发起支付
    if contract.status != 1:
        if contract.status == 0:
            flash("请先签署合同后再进行支付", "warning")
        elif contract.status == 4:
            flash("该合同已支付完成", "info")
        else:
            flash("该合同当前状态无法支付 (可能已撤销或已到期)", "error")
        return redirect(url_for('contract.view_contracts'))

    # 获取房屋信息 (保持不变)
    channel = PrivateChannelModel.query.get(contract.channel_id)
    if not channel:
        flash("找不到关联合同的频道信息", "error")
        return redirect(url_for('contract.view_contracts'))

    house = HouseInfoModel.query.get(channel.house_id)
    if not house:
        flash("找不到关联的房屋信息", "error")
        return redirect(url_for('contract.view_contracts'))

    alipay = alipay_obj()

    # 金额（转为字符串），可以根据你的合同字段
    total_amount = str(contract.total_amount)
    subject = f"租房合同支付 - {house.house_name}（{house.addr}）"

    out_trade_no = str(int(time.time() * 1000)) + str(random.randint(1000, 9999))
    # 将订单号与合同ID关联存储，以便回调时使用
    session[f'payment_pending_{out_trade_no}'] = contract.id


    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=out_trade_no,
        total_amount=total_amount,
        subject=subject,
        return_url=ALIPAY_SETTING.get('ALIPAY_RETURN_URL'),
        notify_url=ALIPAY_SETTING.get('ALIPAY_NOTIFY_URL')
    )

    url = ALIPAY_SETTING.get('APIPAY_GATEWAY') + '?' + order_string
    return redirect(url)
