#### 配置信息
- 由于社区条例，本项目配置未在源文件中
- 在项目根目录新建config.py，以下是内容
SECRET_KEY = ''


> 数据库配置信息
HOSTNAME = ''
PORT = ''
DATABASE = ''
USERNAME = ''
PASSWORD = ''
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


> 邮箱配置
MAIL_SERVER = '
MAIL_PORT = 465
MAIL_USE_SSL = True
> MAIL_SSL仅能使用中文
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ''


> 应用的基础域名，用于支付宝回调等
APP_DOMAIN = ''

> 文件上传配置
import os

> 上传文件夹配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

> 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

> 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


> 阿里云 OSS 配置
OSS_ACCESS_KEY_ID = ''
OSS_ACCESS_KEY_SECRET = ''
OSS_BUCKET_NAME = ''
OSS_ENDPOINT = "oss-cn-shenzhen.aliyuncs.com"
OSS_REGION = "cn-shenzhen"  # <--- 例如，如果您的Bucket在杭州，则填写 "cn-hangzhou"

> DeepSeek AI Chat Configuration
DEEPSEEK_API_KEY = ''
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
