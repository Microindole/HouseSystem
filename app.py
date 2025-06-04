import json
from datetime import datetime

import redis
from flask import Flask, render_template, g, session, request
from flask_apscheduler import APScheduler

from flask import Flask, render_template, g, session, request
import config
from blueprints.contract import contract_bp
from blueprints.logging import logging_bp
from exts import db, mail
from flask_migrate import Migrate
from blueprints.account import account_bp
from blueprints.house import house_bp
from blueprints.feedback import feedback_bp
from blueprints.sandbox import pay_bp
from blueprints.ai_chat_bp import ai_chat_bp
from models import MessageModel, ComplaintModel, DailyRentRateModel, HouseStatusModel
from task.visit_tasks import store_daily_visit_stats
from decorators import login_required, verify_token


app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(house_bp, url_prefix='/house')
app.register_blueprint(feedback_bp, url_prefix='/feedback')
app.register_blueprint(contract_bp, url_prefix='/contract')

app.register_blueprint(logging_bp, url_prefix='/logging')
app.register_blueprint(pay_bp, url_prefix='/') # 注册 pay_bp
app.register_blueprint(ai_chat_bp)

with open('static/json/cities.json', 'r', encoding='utf-8') as f:
    cities_data = json.load(f)


@app.context_processor
def inject_cities_data():
    return dict(cities_data=cities_data)


@app.context_processor
def inject_default_filters():
    return dict(filters={"keyword": "", "region": "", "city": ""})


@app.context_processor
def inject_unread_counts():
    unread_total = 0
    unread_complaint_updates = 0
    if hasattr(g, 'username'):
        username = g.username
        unread_channels = db.session.query(MessageModel.channel_id)\
            .filter(MessageModel.receiver_username == username, MessageModel.is_read == False)\
            .distinct().count()
        unread_total = unread_channels

        unread_complaint_updates = ComplaintModel.query.filter(
            ComplaintModel.sender == username,
            ComplaintModel.status != '待处理',
            ComplaintModel.update_seen_by_sender == False
        ).count()

    return dict(unread_total=unread_total, unread_complaint_updates=unread_complaint_updates)


@app.context_processor
def inject_user_info():
    return dict(g=g)


@app.before_request
def set_default_filters():
    g.filters = {
        'region': '',
        'rooms': '',
        'min_price': None,
        'max_price': None
    }


@app.before_request
def inject_user_from_token():
    token = request.cookies.get('access_token')
    if token:
        payload = verify_token(token)
        if payload:
            g.username = payload.get('username')
            g.user_type = payload.get('user_type')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tenant/home')
def tenant_home():
    return "租客首页"


@app.route('/landlord/home')
def landlord_home():
    return "房东首页"


@app.route('/admin/dashboard')
def admin_dashboard():
    return "管理后台"

r = redis.Redis(host='localhost', port=6379, db=0)

def record_ip_visit():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    today_key = 'visits:' + datetime.now().strftime('%Y%m%d')
    r.sadd(today_key, ip)


@app.before_request
def before_request():
    if request.endpoint != 'static':
        record_ip_visit()

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
print("[Scheduler] APScheduler 启动完成")


@scheduler.task('cron', id='daily_visit_stats', hour=0, minute=5)
def scheduled_task():
    from task.visit_tasks import store_daily_visit_stats
    with app.app_context():
        store_daily_visit_stats()

@app.route('/test/save_visit')
def test_save():
    store_daily_visit_stats()
    return "测试写入成功"



if __name__ == '__main__':
    app.run(debug=True)