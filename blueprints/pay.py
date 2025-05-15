# 支付宝支付相关配置
import os
from alipay import AliPay, DCAliPay, ISVAliPay
import config

ALIPAY_SETTING = {
    'ALIPAY_APP_ID': "2021000148677978",  # 去沙箱找应用ID
    'ALIPAY_DEBUG': False,
    'APIPAY_GATEWAY': "https://openapi-sandbox.dl.alipaydev.com/gateway.do",  # 沙盒环境的网关
    'ALIPAY_RETURN_URL': f"{config.APP_DOMAIN}/alipay/success_result/",  # 同步回调网址--用于前端,支付成功之后回调
    'ALIPAY_NOTIFY_URL': f"{config.APP_DOMAIN}/alipay/fail_result/",  # 异步回调网址---后端使用，post请求，网站未上线，post无法接收到响应内容，付成功之后回调
    'APP_PRIVATE_KEY_STRING': './private.pem',  # 自己生成的私钥
    # 支付宝的公钥
    'ALIPAY_PUBLIC_KEY_STRING': './public.pem',  # 一定要注意，是支付宝给你的公钥，不是你自己生成的那个
    'SIGN_TYPE': "RSA2"
}
# 生成支付alipay对象，以供调用
def alipay_obj():
    alipay = AliPay(
        appid=ALIPAY_SETTING.get('ALIPAY_APP_ID'),
        app_notify_url=None,  # 默认回调 url
        app_private_key_string=open(ALIPAY_SETTING.get('APP_PRIVATE_KEY_STRING')).read(),
        alipay_public_key_string=open(ALIPAY_SETTING.get('ALIPAY_PUBLIC_KEY_STRING')).read(),
        sign_type=ALIPAY_SETTING.get('SIGN_TYPE'),
        debug=ALIPAY_SETTING.get('ALIPAY_DEBUG'),
        verbose=False,  # 输出调试数据
        # config=AliPayConfig(timeout=50)  # 可选，请求超时时间
    )
    return alipay
# print(alipay_obj())