import requests
# import selenium
from bs4 import BeautifulSoup
import datetime
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

# 请求登录
url = "https://www.kanzhiqiu.com/user/login.htm"
# session()和sessions()的区别
session = requests.session()
session.post(url, headers=headers, data=form_data)

# 登录后获取内容
today = datetime.date.today()
startdate = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=00, minute=00, second=00)
enddate = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=55, second=00)

keywords = ["铁矿石", "动力煤", "铜", "黄金", "玉米", "豆粕", "橡胶", "原油", "风电"]
# response = session.get('https://www.kanzhiqiu.com/newreport/', headers=headers)
params = {
    "search": "铁矿石",
    # 默认是DATE_LIMIT_YEAR, 现在要改成DATE_LIMIT_DAYS
    "dateLimit": "",
    "startDate": startdate,
    "endDate": enddate,
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

# 模拟翻页

# 初筛
soup = BeautifulSoup(html, "lxml")
tag = soup.div
tag['class'] = "globalSearch_list"



