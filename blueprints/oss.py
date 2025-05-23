# BluePrint/oss.py
from flask import Blueprint, request, jsonify, current_app
import alibabacloud_oss_v2 as oss
from alibabacloud_oss_v2.credentials import StaticCredentialsProvider
from werkzeug.utils import secure_filename
import uuid
import os

from models import HouseInfoModel as HouseInfo  # 确保路径正确
from exts import db  # 确保路径正确

oss_bp = Blueprint('oss', __name__, url_prefix='/oss')


def allowed_file(filename):
    """检查文件扩展名是否被允许"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def get_oss_client():
    """初始化并返回OSS客户端"""
    access_key_id = current_app.config['OSS_ACCESS_KEY_ID']
    access_key_secret = current_app.config['OSS_ACCESS_KEY_SECRET']
    endpoint = current_app.config['OSS_ENDPOINT']
    region = current_app.config.get('OSS_REGION') 
    # 调试日志：检查加载的配置值
    current_app.logger.info(
        f"Loaded OSS_ACCESS_KEY_ID (first 5 chars): {str(access_key_id)[:5] if access_key_id else 'Not Set'}")
    current_app.logger.info(f"Loaded OSS_ENDPOINT: {endpoint}")
    current_app.logger.info(f"Loaded OSS_REGION: {region}")
    # ... (后续的配置检查和客户端初始化代码) ...

    if not all([access_key_id, access_key_secret, endpoint]):
        raise ValueError("OSS配置不完整 (ID, Secret, Endpoint 必须提供)")
    if access_key_id == "YOUR_ACCESS_KEY_ID" or access_key_secret == "YOUR_ACCESS_KEY_SECRET":
        current_app.logger.warning("正在使用默认的OSS占位符凭证，请配置真实的凭证！")

    credentials_provider = StaticCredentialsProvider(access_key_id, access_key_secret)

    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.endpoint = endpoint
    # 如果您的endpoint不包含region信息，或者您想显式指定region, 可以取消注释下一行
    cfg.region = region # 例如 'cn-hangzhou'

    return oss.Client(cfg)


@oss_bp.route('/upload_house_image/<int:house_id>', methods=['POST'])
def upload_house_image(house_id):
    """
    上传房屋图片到OSS，并将URL更新到对应的房屋信息中。
    前端应以 multipart/form-data 形式发送图片，字段名为 'image'。
    """
    if 'image' not in request.files:
        return jsonify(success=False, message="请求中未找到图片文件(字段名应为'image')"), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify(success=False, message="未选择任何图片文件"), 400

    if not allowed_file(file.filename):
        return jsonify(success=False, message="文件类型不被允许"), 400

    # 查找对应的房屋信息
    house = db.session.get(HouseInfo, house_id)  # 使用 db.session.get 替代 query.get
    if not house:
        return jsonify(success=False, message=f"ID为 {house_id} 的房屋信息未找到"), 404

    try:
        client = get_oss_client()
        bucket_name = current_app.config['OSS_BUCKET_NAME']

        # 生成安全且唯一的文件名
        s_filename = secure_filename(file.filename)
        file_ext = os.path.splitext(s_filename)[1]
        # 使用UUID确保文件名唯一，并组织到特定房屋ID的目录下
        object_name = f"house_images/{house_id}/{uuid.uuid4().hex}{file_ext}"

        # 上传文件
        # file.stream 提供了文件内容的流式读取
        result = client.put_object(oss.PutObjectRequest(
            bucket=bucket_name,
            key=object_name,
            body=file.stream,  # 或者 file.read() 如果文件不大
            headers = {"x-oss-object-acl": "public-read"}
        ))

        if result.status_code == 200:
            # 构建图片URL
            # 优先使用自定义CNAME域名
            oss_cname_url = current_app.config.get('OSS_CNAME_URL')
            if oss_cname_url:
                # 确保CNAME URL末尾没有斜杠，object_name开头没有斜杠
                image_url = f"{oss_cname_url.rstrip('/')}/{object_name.lstrip('/')}"
            else:
                # 否则使用标准的OSS域名格式
                image_url = f"https://{bucket_name}.{current_app.config['OSS_ENDPOINT']}/{object_name}"

            # 更新数据库中的图片URL
            house.image_url = image_url
            db.session.commit()

            current_app.logger.info(
                f"图片上传成功: {image_url}, Status: {result.status_code}, Request ID: {result.request_id}")
            return jsonify(success=True, message="图片上传成功", image_url=image_url, house_id=house_id), 200
        else:
            current_app.logger.error(f"OSS上传失败: Status: {result.status_code}, Request ID: {result.request_id}")
            return jsonify(success=False, message=f"OSS上传失败，状态码: {result.status_code}"), 500

    except ValueError as ve:  # OSS配置错误
        current_app.logger.error(f"OSS配置错误: {ve}")
        return jsonify(success=False, message=f"服务器OSS配置错误: {ve}"), 500
    # except oss.exceptions.ClientError as ce:  # OSS SDK客户端错误
    #     current_app.logger.error(f"OSS客户端错误: {ce}")
    #     return jsonify(success=False, message=f"OSS操作失败: {ce.message}"), 500

    except Exception as e:
        current_app.logger.error(f"上传图片时发生未知错误: {e}")
        db.session.rollback()  # 如果发生错误，回滚数据库更改
        return jsonify(success=False, message=f"服务器内部错误: {str(e)}"), 500