import requests
from bs4 import BeautifulSoup
import datetime
import re

keywords = ["铁矿石", "动力煤", "铜", "黄金", "玉米", "豆粕", "橡胶", "原油", "风电"]
today = datetime.date.today()
startDate = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=00, minute=00, second=00)
endDate = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=55, second=00)

# 请求登录
# cookies中有JSESSIONIDVERSION=2f:2，是随机生成的不知道如何跳过
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
}
form_data = {
    "signonForwardAction": "",
    "login_submit": "1",
    "newlogin": "",
    "username": "18701877496",
    "password": "kyb975",
    "j_captcha_response": "",
    "remember_name": "1"
}
url = "https://www.kanzhiqiu.com/user/login.htm"
# session()和sessions()的区别
session = requests.session()
session.post(url, headers=headers, data=form_data)

# 初筛
def judge(article, key="铁矿石"):
    # pattern = re.compile("([\u4e00-\u9fa5]*(铁矿石)[\u4e00-\u9fa5]*)|[a-zA-z0-9=\.-_]*(铁矿石)")
    pattern = re.compile("[\u4e00-\u9fa5]*(铁矿石)[\u4e00-\u9fa5]*")
    index = []
    for i, a in enumerate(article):
        flag = 0
        for k, v in a.items():
            if k != "link":
                result = re.findall(pattern, v)
                flag = flag + len(result)
        if flag == 0:
            index.append(i)
    for i in index:
        del article[i]
    return article

# 登录后获取页面内容
def get_total_article(session, page, keyword="铁矿石"):
    article_list = []
    domain = "https://www.kanzhiqiu.com/"
    params = {
        "search": keyword,
        # 默认是DATE_LIMIT_YEAR, 现在要改成DATE_LIMIT_DAYS
        "dateLimit": "",
        "startDate": startDate,
        "endDate": endDate,
        # NEWS为公众号, CJAUTONEWS为新闻官媒, CJCAST, EVENT为快讯, REPORT, CONF为研究报告
        # 这里可能会有问题
        "type": "NEWS,BULLETIN,THIRDMARKETGG,HKMARKETGG,REPORT,RATINGREPORT,BONDGG,BONDGG_2,CONF,INVESTOR,CJCAST,CUSTOMERDOC,CJAUTONEWS",
        "page": page,
        "pageSize": "10",
        "highlightLevel": "1",
        "boostReduction": "true",
        "hyperSearchFields": "all",
        "timeOut": "200",
        "sortByTime": "true",
        "clickFrom": "0",
        "errorCollect": "true"
    }

    response = session.post('https://www.kanzhiqiu.com/newsadapter/fulltextsearch/fulltext_search.htm', data=params)
    html = response.content.decode()
    # print(html)

    soup = BeautifulSoup(html, "lxml")
    tag = soup.div
    article = tag.find_all("div", "globalSearch_list")

    for arti in article:
        temp = {}
        # 处理header标题是否有关键字
        # get_text()能够获取节点及子节点的全部文本节点
        # 处理字符串中大量的空格
        # 1、
        # 2、
        # 3、
        # 4、
        temp["content"] = str(arti.h3.get_text()).replace("\n", "")
        temp["link"] = domain + str(arti.h3.a["href"])
        desc = arti.find_all("div", "globalSearch_list_con")
        for d in desc:
            text = d.get_text()
            temp["text"] = text.replace(" ", "")
        article_list.append(temp)
        # 模式匹配关键字，筛选后加入列表
    article_list = judge(article_list)
    print(article_list)

for keyword in keywords:
    params = {
        "search": keyword,
        # 默认是DATE_LIMIT_YEAR, 现在要改成DATE_LIMIT_DAYS
        "dateLimit": "",
        "startDate": startDate,
        "endDate": endDate,
        # NEWS为公众号, CJAUTONEWS为新闻官媒, CJCAST, EVENT为快讯, REPORT, CONF为研究报告
        # 这里可能会有问题
        "type": "NEWS,BULLETIN,THIRDMARKETGG,HKMARKETGG,REPORT,RATINGREPORT,BONDGG,BONDGG_2,CONF,INVESTOR,CJCAST,CUSTOMERDOC,CJAUTONEWS",
        "page": "1",
        "pageSize": "10",
        "highlightLevel": "1",
        "boostReduction": "true",
        "hyperSearchFields": "all",
        "timeOut": "200",
        "sortByTime": "true",
        "clickFrom": "0",
        "errorCollect": "true"
    }

    response = session.post('https://www.kanzhiqiu.com/newsadapter/fulltextsearch/fulltext_search.htm', data=params)
    html = response.content.decode()
    # print(html)

    soup = BeautifulSoup(html, "lxml")
    tag = soup.div
    # 模拟翻页
    page_list = tag.find(id="pageSet").find_all("a")
    total = int(page_list[-3].get_text())
    for p in range(2, total):
        get_total_article(session, p, keyword)





