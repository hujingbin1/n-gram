from lxml import etree
import csv
import re

# 原始文件路径
dat_file_path = '.\\dataset\\news_tensite_xml.smarty.dat'
# 输出的CSV文件路径
csv_file_path = './data.csv'

# 自动修正XML内容的函数
def auto_correct_xml_content(content):
    # 替换非法的 & 符号
    corrected_content = re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', content)
    return corrected_content

# 读取.dat文件内容
with open(dat_file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

# 自动修正内容
corrected_content = auto_correct_xml_content(file_content)

# 将内容包裹在<root>标签内，以创建一个有效的XML结构
wrapped_content = f'<root>{corrected_content}</root>'

# 解析修正后的XML内容
root = etree.fromstring(wrapped_content.encode('utf-8'))

# 准备写入CSV文件
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    # 定义列标题
    writer.writerow(['contenttitle', 'content'])

    # 遍历每个<doc>元素提取信息
    for doc in root.findall('.//doc'):
        contenttitle = doc.find('.//contenttitle').text if doc.find('.//contenttitle') is not None else ''
        content = doc.find('.//content').text if doc.find('.//content') is not None else ''
        writer.writerow([contenttitle, content])  # 写入内容

print("转换完成，文件保存至:", csv_file_path)
