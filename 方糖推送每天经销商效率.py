
# coding: utf-8

# In[ ]:

'''
Created on 2018-4-20

例子:美国时间每天8:2，中国时间19:2 执行数据推送
'''
import datetime
import threading

def report_mouthly_sales():
    from threading import Timer
    import os
    os.sys.path.append('/Users/apple/Desktop/')
    import bog
    import requests
    url_ = "https://sc.ftqq.com/SCU36515T35dc04456ad6f3a509cf530de7221e135bfcf9d82a8d7.send"
    title = u"经销商本月出货"
    content = str(bog.distributor_this_mouth_sales())
    data = {
       "text":title,
       "desp":content
    }

    req = requests.get(url_,params= data)
    t = Timer(86400,report_mouthly_sales)
    t.start()

# 获取现在时间
now_time = datetime.datetime.now()
# 获取明天时间
next_time = now_time + datetime.timedelta(days=+1)
next_year = next_time.date().year
next_month = next_time.date().month
next_day = next_time.date().day
# 获取明天3点时间
next_time = datetime.datetime.strptime(str(next_year)+"-"+str(next_month)+"-"+str(next_day)+" 8:02:00", "%Y-%m-%d %H:%M:%S")
# # 获取昨天时间
# last_time = now_time + datetime.timedelta(days=-1)

# 获取距离明天3点时间，单位为秒
timer_start_time = (next_time - now_time).total_seconds()
print(timer_start_time)
# 54186.75975


#定时器,参数为(多少时间后执行，单位为秒，执行的方法)
timer = threading.Timer(timer_start_time, report_mouthly_sales)
timer.start()

