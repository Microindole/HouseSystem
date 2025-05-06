import json

from flask import Flask, render_template, g, session
import config
from exts import db
from flask_migrate import Migrate
from blueprints.account import account_bp
from blueprints.house import house_bp
from blueprints.feedback import feedback_bp
from models import MessageModel

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)
db.init_app(app)

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
def inject_unread_total():
    username = session.get('username')
    if username:
        unread_total = MessageModel.query.filter_by(receiver_username=username, is_read=False).count()
    else:
        unread_total = 0
    return dict(unread_total=unread_total)

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
