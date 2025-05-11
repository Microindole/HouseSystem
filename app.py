import json

from flask import Flask, render_template, g, session
import config
from exts import db, mail
from flask_migrate import Migrate
from blueprints.account import account_bp
from blueprints.house import house_bp
from blueprints.feedback import feedback_bp
from models import MessageModel, ComplaintModel, DailyRentRateModel, HouseStatusModel


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
    if 'username' in session:
        username = session['username']
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


@app.before_request
def set_default_filters():
    g.filters = {
        'region': '',
        'rooms': '',
        'min_price': None,
        'max_price': None
    }


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


if __name__ == '__main__':
    app.run(debug=True)