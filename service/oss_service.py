import os
import uuid
import alibabacloud_oss_v2 as oss_sdk
from alibabacloud_oss_v2.credentials import StaticCredentialsProvider
from flask import current_app

def get_oss_client():
    access_key_id = current_app.config.get('OSS_ACCESS_KEY_ID')
    access_key_secret = current_app.config.get('OSS_ACCESS_KEY_SECRET')
    endpoint = current_app.config.get('OSS_ENDPOINT')
    region = current_app.config.get('OSS_REGION')
    if not all([access_key_id, access_key_secret, endpoint]) or \
       access_key_id == "YOUR_ACCESS_KEY_ID" or access_key_secret == "YOUR_ACCESS_KEY_SECRET":
        raise ValueError("OSS配置不完整或使用了默认占位符凭证。请检查应用的OSS配置。")
    credentials_provider = StaticCredentialsProvider(access_key_id, access_key_secret)
    cfg = oss_sdk.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.endpoint = endpoint
    if region:
        cfg.region = region
    return oss_sdk.Client(cfg)

def delete_oss_object(image_url):
    if not image_url or not image_url.startswith('http'):
        return False
    try:
        bucket_name = current_app.config['OSS_BUCKET_NAME']
        oss_endpoint = current_app.config['OSS_ENDPOINT']
        oss_cname_url = current_app.config.get('OSS_CNAME_URL', '').rstrip('/')
        object_key = None
        if oss_cname_url and image_url.startswith(oss_cname_url + '/'):
            object_key = image_url.split(oss_cname_url + '/', 1)[1]
        else:
            endpoint_domain_part = oss_endpoint.replace('https://', '').replace('http://', '')
            standard_oss_url_prefix_https = f"https://{bucket_name}.{endpoint_domain_part}/"
            standard_oss_url_prefix_http = f"http://{bucket_name}.{endpoint_domain_part}/"
            if image_url.startswith(standard_oss_url_prefix_https):
                object_key = image_url.split(standard_oss_url_prefix_https, 1)[1]
            elif image_url.startswith(standard_oss_url_prefix_http):
                object_key = image_url.split(standard_oss_url_prefix_http, 1)[1]
        if object_key:
            client = get_oss_client()
            req = oss_sdk.DeleteObjectRequest(bucket_name, object_key)
            client.delete_object(req)
            return True
        else:
            return False
    except Exception:
        return False

