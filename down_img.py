import os
import hashlib
import requests
from PIL import Image
from io import BytesIO

# 作用:下载指定 URL 的图片，将其转换为 WebP 格式，并保存到本地指定目录。

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
    image_url = "https://datascientest.com/en/files/2023/11/mysql.webp"  # 替换为实际的图片 URL
    #image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSK3XzeNSfofI2fbLJ87dFpGBOSmygV1F_LgQ&s"  # 替换为实际的图片 URL
    download_and_convert_image(image_url)
