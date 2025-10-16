# import os
#
# class Config:
#     # 从环境变量中读取 SECRET_KEY，如果未设置则使用默认值
#     SECRET_KEY = os.getenv('SECRET_KEY', 'wonwigfoniuegfbnkco')

SECRET_KEY = "xxx"


# 数据库配置信息
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'flask_house'
USERNAME = 'root'
PASSWORD = 'xxx'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


# 邮箱配置
MAIL_SERVER = 'smtp.xxx.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
# MAIL_SSL仅能使用中文
MAIL_USERNAME = 'xxx@xxx.com'
MAIL_PASSWORD = 'xxx'
MAIL_DEFAULT_SENDER = 'xxx@xxx.com'


# 应用的基础域名，用于支付宝回调等
APP_DOMAIN = "http://xxx"

# 文件上传配置
import os

# 上传文件夹配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


 # 阿里云 OSS 配置
OSS_ACCESS _KEY_ID = 'xxx'
OSS_ACCESS _KEY_SECRET = 'xxx'
OSS_BUCKET_NAME = "house-system"
# OSS_ENDPOINT 通常是 Bucket 所在地域的访问域名，例如：oss-cn-hangzhou.aliyuncs.com
# 请参考OSS文档获取正确的Endpoint：https://help.aliyun.com/document_detail/31837.html
OSS_ENDPOINT = "oss-cn-shenzhen.aliyuncs.com"
OSS_REGION = "cn-shenzhen"  # <--- 例如，如果您的Bucket在杭州，则填写 "cn-hangzhou"
# (可选) 如果您想为上传的文件指定一个自定义域名（需在OSS控制台配置CNAME）
# OSS_CNAME_URL = os.environ.get('OSS_CNAME_URL') or None  # 例如: "https://img.yourdomain.com"

# DeepSeek AI Chat Configuration
DEEPSEEK_API_KEY = "sk-xxx"  # 这是你提供的密钥
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
