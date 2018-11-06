
# coding: utf-8

from __future__ import unicode_literals
from threading import Timer
from wxpy import *
import requests

import pandas as pd
url = 'https://raw.githubusercontent.com/bog5d/Feng-chao/master/%E5%85%8D%E8%BE%85%E6%9D%90%E4%BF%83%E9%94%80%E7%BB%9F%E8%AE%A1.csv'

data = pd.read_csv(url)

x = data.groupby('客户姓名').agg(sum).nlargest(n=50,columns='红包金额')
x = x.reset_index()
x =x[['客户姓名','红包金额','辅材使用']]
x.columns = ['姓名','已领红包','销售数量']
x['排名']=x.index+1
x =x[['排名','姓名','已领红包','销售数量']]

x[' '] = '  '
x = x.set_index(' ')
def tuisong(x):
     return str(x)
def mingci(x):
    return "第"+str(x)+'名，'

x['tuisong']=x['排名'].apply(mingci)+x.姓名.apply(tuisong)+'，销售，'+x.销售数量.apply(tuisong)+'台；'+'已领取红包，'\
+x['已领红包'].apply(tuisong)+'元。'

s3 = x['tuisong']


bot = None

def get_news1():
    
    return x.tuisong

def login_wechat():
    
    global bot
    bot = Bot()
    # bot = Bot(console_qr=2,cache_path="botoo.pkl")#Linux专用，像素二维码
 
def send_news():
    if bot == None:
        login_wechat()
    try:
        my_friend = bot.friends().search(u'王波')[0]    #你朋友的微信名称，不是备注，也不是微信帐号。
        # my_group = bot.groups().search(u'大副')[0]    #你群的微信名称，不是备注，也不是微信帐号。
        my_friend.send(get_news1())
        # my_group.send(get_news1())
        t = Timer(600, send_news) #每86400秒（1天），发送1次，不用linux的定时任务是因为每次登陆都需要扫描二维码登陆，很麻烦的一件事，就让他一直挂着吧
        t.start()
    except:
        print(u"今天消息发送失败了")
if __name__ == "__main__":
    send_news()



