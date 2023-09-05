import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
import time

from selenium.webdriver import Keys

author_url = ''
driver = webdriver.Edge()
driver.get(author_url)

print("正在获取文章列表……")

# 模拟向下滚动页面，以加载更多内容
while True:
    js = "window.scrollTo(0, document.body.scrollHeight)"
    driver.execute_script(js)  # 模拟鼠标滚轮，滑动页面至底部
    # 等待一段时间，确保内容加载完成
    time.sleep(0.5)

    # 检查是否已经到达页面底部
    if driver.execute_script("return window.innerHeight + window.pageYOffset >= document.body.scrollHeight"):
        break

print("获取完成！开始爬取")

# 获取作者首页信息
html_content = driver.page_source

# 使用Beautiful Soup解析HTML内容
soup = BeautifulSoup(html_content, 'html.parser')

# 找到包含文章列表的父元素
article_list = soup.find('ul', class_='note-list')

sum = 0

# 遍历每个文章列表项
for article_item in article_list.find_all('li'):

    sum = sum + 1

    # 找到标题所在的<a>标签元素（类名为'title'）
    title_element = article_item.select_one('a.title')

    if title_element:
        # 提取文章标题文本与URL
        title = title_element.text
        href = title_element.get('href')
        href = 'https://www.jianshu.com' + href


        ua = UserAgent()
        headers = {'User-Agent': ua.random}  # 请求头
        article_url = href

        response = requests.get(article_url, headers=headers)  # 发起请求 简书需要添加headers
        soup = BeautifulSoup(response.text, 'html.parser')

        article = soup.find('article', class_='_2rhmJa')  # 使用标签和类名定位

        if article:
            # 打印文章标题与URL
            print('当前编号' + str(sum) + '，标题：《' + title + '》，链接：' + href)
        else:
            print('出现问题')
            continue

        # 获取时间并替换冒号
        article_time = soup.find('time')

        if article_time:
            article_time = article_time.get_text()
        else:
            article_time = 'null'

        article_time = article_time.replace(':', '.')

        article_html = article.prettify()  # 将文章对象转换为格式化的HTML字符串
        article_text = BeautifulSoup(article_html, 'html.parser').get_text()

        with open('《' + title + '》' + article_time + '.txt', 'w', encoding='utf-8') as file:
            file.write(article_text)

print('爬取完成！共' + str(sum) + '篇文章')
