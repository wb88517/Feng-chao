# coding: utf-8
from __future__ import unicode_literals
from threading import Timer
from wxpy import *
import requests
import pandas as pd 
import numpy as np

url = 'https://raw.githubusercontent.com/bog5d/Feng-chao/master/profit.csv'

#prof = pd.read_excel('/Users/apple/Downloads/销售毛利明细表20181016.xlsx',sep='\t',header=2).fillna('/')
prof = pd.read_csv(url,header=2,sep=',').fillna('/')
prof['单据类型'] = prof['单据类型'].replace(r'往来销售',np.nan,regex=True)

prof= prof.fillna(method='pad')
prof = prof.loc[~(prof['单据日期']=='/')]
#pd.to_datetime('单据日期')
prof['单据日期']= pd.to_datetime(prof['单据日期'])
prof = prof.set_index('单据日期')
prof = prof[['单据类型',  '客户名称', '数量', '销售价', '成本价', '销售收入', '销售成本',
       '销售毛利', '销售毛利率']].rename(columns={'单据类型':'型号'})
#prof.loc[(prof['客户名称'].isin(old_dealer))]

# 参考 liutong['所属业务'],liutong['客户名称']=liutong['客户名称'].str.split('-',1).str
prof['对接业务'],prof['客户名称'] = prof['客户名称'].str.split('-',1).str


prof1 = prof.loc[(prof['型号'].str.contains('水器')&~prof['型号'].str.contains('空壳'))]
sale_num = prof1.groupby('对接业务').sum()[['数量','销售收入']].nlargest(n=100,columns='数量')
sale_num = sale_num.reset_index()



sale_num_all = sale_num.loc[sale_num['对接业务'].str.contains('王海梦|李锟|王思密|商渠及其他客户')]
y = sale_num_all

def tuisong(x):
     return str(x)
def mingci(x):
    return "第"+str(x)+'名，'
y=y.copy()
y['tuisong']="截止目前"+y['对接业务'].apply(tuisong)+'区域，出货总数量为'\
+y.数量.apply(tuisong)+'台，销售金额'+y.销售收入.apply(tuisong)+'元'

y[' '] = '  '
y = y.set_index(' ')
s1 = y['tuisong']
s1






prof2 = prof1['2018-11'].copy()
sale_num_this_mouth = prof2.groupby('对接业务').sum()[['数量','销售收入']].nlargest(n=100,columns='数量').reset_index()
sale_num_this_mouth = sale_num_this_mouth.loc[sale_num['对接业务'].str.contains('王海梦|李锟|王思密|商渠及其他客户')]

# 修改列名
sale_num_this_mouth.columns=['对接业务', '出货数量', '出货金额']


sale_dict ={'王海梦':800000,
            '李锟':1200000,
            }
sale_num_this_mouth['本月出货目标'] = sale_num_this_mouth['对接业务'].map(sale_dict)

sale_num_this_mouth['完成率']= (sale_num_this_mouth['出货金额']/sale_num_this_mouth['本月出货目标'])

sale_num_this_mouth = sale_num_this_mouth.fillna(0)

def s_rate(x):
    if x > 0:
        return str(100 *round(x,3))+'%'
    else:
        return '0%'
        
sale_num_this_mouth['完成率'] = sale_num_this_mouth['完成率'].apply(s_rate)

def s_short(x):
    if len(x)>4:
        return x[0:3]+'%'
    else:
        return x
sale_num_this_mouth['完成率'] = sale_num_this_mouth['完成率'].apply(s_short)
y = sale_num_this_mouth

y=y.copy()
y['tuisong']="本月,"+y['对接业务'].apply(tuisong)+'区域，出货'\
+y.出货数量.apply(tuisong)+'台，总额'+y.出货金额.apply(tuisong)+'元'\
+ '；本月出货目标'+y.本月出货目标.apply(tuisong)+'，进度'+y['完成率'].apply(tuisong)

y[' '] = '  '
y = y.set_index(' ')
y = y.loc[y['对接业务'].str.contains('王海梦|李锟|王思密|商渠及其他客户')]
s2 = y['tuisong']
s2


# 以下部分为o2o数据通报

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
    
    return s1

def get_news2():
    
    return s2

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
        my_friend.send(get_news2())
        my_friend.send(s3)
        # my_group.send(get_news1())
        t = Timer(86400, send_news) #每86400秒（1天），发送1次，不用linux的定时任务是因为每次登陆都需要扫描二维码登陆，很麻烦的一件事，就让他一直挂着吧
        t.start()
    except:
        print(u"今天消息发送失败了")
if __name__ == "__main__":
    send_news()
