import os
import re
import requests
from PIL import Image
from io import BytesIO
import hashlib


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
        print(f"图片下载成功: {url}")
    else:
        print(f"下载失败: {url}")


def convert_to_webp(image_path):
    """将图片转换为 WebP 格式"""
    with Image.open(image_path) as img:
        webp_path = image_path.rsplit(".", 1)[0] + ".webp"
        img.save(webp_path, "WEBP")
    os.remove(image_path)  # 删除原图
    print(f"图片转换为 WebP 格式: {webp_path}")
    return webp_path


def process_markdown_files(directory):
    """处理指定目录下的所有 Markdown 文件"""
    image_folder = os.path.join(directory, "images")
    os.makedirs(image_folder, exist_ok=True)

    md_pattern = re.compile(r"!\[.*?\]\((http[s]?://.*?)\)")

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)
                with open(md_file_path, 'r', encoding='utf-8') as md_file:
                    content = md_file.read()

                # 查找图片链接
                matches = md_pattern.findall(content)
                for url in matches:
                    # 下载图片
                    image_name = get_md5(url)
                    local_image_path = os.path.join(image_folder, image_name)
                    download_image(url, local_image_path)

                    # 转换为 WebP 格式
                    webp_path = convert_to_webp(local_image_path)

                    # 替换 Markdown 中的图片链接
                    webp_relative_path = os.path.relpath(webp_path, directory)
                    content = content.replace(url, os.path.join("/", webp_relative_path))

                # 写回修改后的内容
                with open(md_file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(content)
                print(f"已处理 Markdown 文件: {md_file_path}")


if __name__ == "__main__":
    md_directory = "/Users/apple/JavaScript/github_hexo_blog/source/_posts"  # 替换为你的 Markdown 文件所在目录
    process_markdown_files(md_directory)
