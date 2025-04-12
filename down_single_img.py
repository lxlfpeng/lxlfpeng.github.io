import os
import re
import requests
from PIL import Image
from io import BytesIO
import hashlib

# Markdown 文件，下载其中的网络图片，将其转换为 WebP 格式，并更新 Markdown 文件中的图片链接，使图片引用指向本地的 WebP 图片文件。这样可以优化图片资源，减少网页加载时间，同时便于管理本地的图片资源。

def get_md5(input_string):
    # 创建 MD5 哈希对象
    md5_hash = hashlib.md5()

    # 更新哈希对象并编码字符串
    md5_hash.update(input_string.encode('utf-8'))

    # 获取十六进制的 MD5 值
    return md5_hash.hexdigest()

def download_image(url, save_path):
    """下载图片并保存到指定路径"""
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"图片下载成功: {url}=>{save_path}")
    else:
        print(f"下载失败: {url}")

def convert_to_webp(image_path):
    """将图片转换为 WebP 格式"""
    current_dir = os.getcwd()
    with Image.open(image_path) as img:
        webp_path = image_path.split('\\')[-1] + ".webp"
        print(f"转换图片路径: {webp_path}")
        image_folder = os.path.join(current_dir, 'source', 'images',webp_path) 
        img.save(image_folder, "WEBP")
    os.remove(image_path)  # 删除原图
    print(f"图片转换为 WebP 格式: {webp_path}")
    return webp_path

def process_markdown_files(md_file_path):
                 # 获取当前工作目录
                current_dir = os.getcwd()
                print(f"当前工作目录: {current_dir}")
                 # 拼接路径
                #markdown_dir = os.path.join(current_dir, 'source', '_posts')
                image_folder = os.path.join(current_dir, 'source', 'images')  
                print(f"图片存储目录: {image_folder}")  
                directory = os.path.join(current_dir, 'source')    
                print(f"Markdown 文件目录: {directory}")
                os.makedirs(image_folder, exist_ok=True)

                md_pattern = re.compile(r"!\[.*?\]\((http[s]?://.*?)\)")
                with open(md_file_path, 'r', encoding='utf-8') as md_file:
                    content = md_file.read()

                # 查找图片链接
                matches = md_pattern.findall(content)
                for url in matches:
                    # 下载图片
                    image_name = get_md5(url)
                    local_image_path = os.path.join(image_folder, image_name)
                    download_image(url, local_image_path)
                    print(f"本地图片路径: {local_image_path}")
                    # 转换为 WebP 格式
                    webp_path = convert_to_webp(local_image_path)
                    print(f"转换后的图片路径: {webp_path}")
                     # 替换 Markdown 中的图片链接
                    # webp_relative_path = os.path.relpath(webp_path, directory)
                    reppath=os.path.join("/", webp_path)
                    print(f"替换后的路径: {reppath}")
                   
                    # print(f"相对路径: {webp_relative_path}")
                    content = content.replace(url,reppath)

                # 写回修改后的内容
                with open(md_file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(content)
                print(f"已处理 Markdown 文件: {md_file_path}")


if __name__ == "__main__":
    markdown_file="source/_posts/黑苹果引导软件之OpenCore.md"  # 替换为实际的 Markdown 文件路径
    process_markdown_files(markdown_file)
