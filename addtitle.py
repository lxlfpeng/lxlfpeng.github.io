import os

# 定义要读取的目录
markdown_dir = "/Users/apple/JavaScript/github_hexo_blog/source/_posts"

# 遍历指定目录下的所有 Markdown 文件
for filename in os.listdir(markdown_dir):
    if filename.endswith(".md"):
        file_path = os.path.join(markdown_dir, filename)

        # 提取文件名（去掉扩展名）
        title = os.path.splitext(filename)[0]

        # 读取原始文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 定义要插入的标题头部
        header = f"---\ntitle: {title}\n---\n\n"

        # 检查文件是否已有 YAML 头部
        if content.startswith("---"):
            # 如果已有头部信息，可以根据实际需求处理 (跳过或修改)
            print(f"文件 {filename} 已经包含头部信息，跳过。")
        else:
            # 在文件头部添加标题信息
            new_content = header + content

            # 将新内容写回文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)

            print(f"已更新文件: {filename}")

print("处理完成！")
