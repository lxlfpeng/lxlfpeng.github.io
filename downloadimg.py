import os
import hashlib
import requests
from PIL import Image
from io import BytesIO

# 下载并转换图片的函数
def download_and_convert_image(image_url, save_dir="source/images"):
    # 获取图片内容
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # 如果请求失败会抛出异常
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image {image_url}: {e}")
        return

    # 使用 MD5 对图片链接进行哈希，生成文件名
    md5_hash = hashlib.md5(image_url.encode('utf-8')).hexdigest()

    # 确保保存目录存在
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 读取图片并转换为 WebP 格式
    try:
        img = Image.open(BytesIO(response.content))
        webp_file_path = os.path.join(save_dir, f"{md5_hash}.webp")
        
        # 转换并保存为 WebP
        img.save(webp_file_path, format="WEBP")
        print(f"Image saved as {webp_file_path}")
    except Exception as e:
        print(f"Error processing image {image_url}: {e}")

# 示例：下载并转换图片
if __name__ == "__main__":
    image_url = "https://img1.baidu.com/it/u=693645169,1871738766&fm=253&fmt=auto&app=138&f=JPEG?w=807&h=500"  # 替换为实际的图片 URL
    download_and_convert_image(image_url)
