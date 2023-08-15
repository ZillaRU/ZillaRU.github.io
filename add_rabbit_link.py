import os
from bs4 import BeautifulSoup


def add_css_to_file(css_file_path, css_content):
    with open(css_file_path, 'a') as f:
        print(css_content)
        f.write(css_content)
        print("CSS done")


def add_hyperlink_to_files(folder_path, css_file_path):
    # 添加 CSS 样式到指定的 CSS 文件
    css_styles = '''

/* 为超链接添加样式 */
.rabbit-link {
    color: pink; /* 设置一般状态下的颜色 */
    text-decoration: none; /* 去除下划线 */
}

/* 鼠标悬停在超链接上的样式 */
.rabbit-link:hover {
    color: red; /* 设置鼠标悬停时的颜色 */
}
'''
    add_css_to_file(css_file_path, css_styles)

    # 递归遍历 site 文件夹中的所有 HTML 文件，并添加超链接
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    print("file_path: ", file_path)
                    # 解析 HTML 文件
                    soup = BeautifulSoup(f, 'html.parser')
                    # 查找包含 class 为 "md-footer-meta md-typeset" 的元素
                    elements = soup.find_all(
                        class_="md-footer-meta md-typeset")
                    for element in elements:
                        # 创建超链接元素
                        link = soup.new_tag(
                            "a", href="https://yliuhz.github.io", class_="my-link")
                        link.string = "看看❤️老兔子❤️忙啥呢～"
                        # 将超链接元素添加到元素中
                        element.append(link)
                # 将修改后的 HTML 内容写回到文件中
                with open(file_path, 'w') as f:
                    f.write(str(soup))


# 指定 CSS 文件路径
css_file_path = 'assets/stylesheets/main.8c5ef100.min.css'
# 指定要遍历的文件夹路径
folder_path = '.'

# 将 CSS 样式添加到指定的 CSS 文件中并在 HTML 文件中添加超链接
add_hyperlink_to_files(folder_path, css_file_path)
