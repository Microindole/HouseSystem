import json
import requests
import os
from urllib.parse import urlparse
import time

def download_images_from_json():
    """从JSON文件中读取数据并下载图片"""
    
    # 创建图片保存文件夹
    image_folder = "test-image"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    
    # 读取JSON文件
    json_file_path = "static/json/ke-2025-06-01.json"
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            house_data = json.load(f)
    except FileNotFoundError:
        print(f"JSON文件 {json_file_path} 不存在")
        return
    except json.JSONDecodeError:
        print("JSON文件格式错误")
        return
    
    print(f"开始下载图片，共 {len(house_data)} 个房源")
    
    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://bj.zu.ke.com/',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive'
    }
    
    success_count = 0
    fail_count = 0
    
    for index, house in enumerate(house_data):
        try:
            # 获取图片URL
            image_url = None
            if "lazyloaded src" in house and house["lazyloaded src"]:
                image_url = house["lazyloaded src"]
            elif "lazyload src" in house and house["lazyload src"]:
                image_url = house["lazyload src"]
            
            if not image_url:
                print(f"第 {index + 1} 个房源没有图片URL")
                fail_count += 1
                continue
            
            # 跳过默认占位图
            if "default" in image_url and "250-182" in image_url:
                print(f"第 {index + 1} 个房源是默认占位图，跳过")
                continue
            
            # 解析URL获取文件扩展名
            parsed_url = urlparse(image_url)
            file_extension = os.path.splitext(parsed_url.path)[1]
            if not file_extension:
                file_extension = '.jpg'  # 默认扩展名
            
            # 生成文件名
            house_title = house.get("twoline", f"house_{index + 1}")
            # 清理文件名中的非法字符
            safe_title = "".join(c for c in house_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50]  # 限制文件名长度
            filename = f"{index + 1:03d}_{safe_title}{file_extension}"
            filepath = os.path.join(image_folder, filename)
            
            # 如果文件已存在，跳过
            if os.path.exists(filepath):
                print(f"第 {index + 1} 个图片已存在: {filename}")
                success_count += 1
                continue
            
            # 下载图片
            print(f"正在下载第 {index + 1} 个图片: {filename}")
            response = requests.get(image_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # 保存图片
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ 下载成功: {filename}")
            success_count += 1
            
            # 添加延时避免被封IP
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"✗ 第 {index + 1} 个图片下载失败: {e}")
            fail_count += 1
        except Exception as e:
            print(f"✗ 第 {index + 1} 个图片处理失败: {e}")
            fail_count += 1
    
    print(f"\n下载完成!")
    print(f"成功: {success_count} 张")
    print(f"失败: {fail_count} 张")
    print(f"总计: {len(house_data)} 张")

def create_image_info_file():
    """创建图片信息文件"""
    
    json_file_path = "static/json/ke-2025-06-01.json"
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            house_data = json.load(f)
    except:
        return
    
    info_file = "test-image/image_info.txt"
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write("房源图片信息\n")
        f.write("=" * 50 + "\n\n")
        
        for index, house in enumerate(house_data):
            f.write(f"图片 {index + 1:03d}:\n")
            f.write(f"  标题: {house.get('twoline', 'N/A')}\n")
            f.write(f"  描述: {house.get('content__list--item--des', 'N/A')}\n")
            f.write(f"  价格: {house.get('content__list--item-price', 'N/A')}\n")
            f.write(f"  品牌: {house.get('brand', 'N/A')}\n")
            f.write(f"  链接: {house.get('content__list--item--aside href', 'N/A')}\n")
            f.write(f"  图片URL: {house.get('lazyloaded src') or house.get('lazyload src', 'N/A')}\n")
            f.write("-" * 30 + "\n")
    
    print(f"图片信息已保存到: {info_file}")

if __name__ == "__main__":
    print("开始爬取房源图片...")
    download_images_from_json()
    print("\n创建图片信息文件...")
    create_image_info_file()
    print("所有任务完成!")