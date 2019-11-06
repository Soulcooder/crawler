'''
  first_commit
'''
import pandas as pd
import datetime as dt

def date_trans(d):
    print(d.to_pydatetime())
    return dt.datetime.strftime(d.to_pydatetime(), "%Y-%m-%d")
# 生成9月27号-11月5号的日期
date = pd.date_range("2019-09-26", "2019-11-05", freq="B").to_list()
tdate = []
for d in date:
    tdate.append(date_trans(d))
