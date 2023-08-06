from resset.__init__ import *
import pandas as pd
import datetime

# 持久化对象
class Context():
    def __init__(self):
        # 账户信息
        self.permission = pd.DataFrame()
        self.userid = ''
    def __repr__(self):
        return "Context({'userid':%s})"\
               %(self.userid)
context = Context()

#判断是否登陆，剩余流量
def query_permission(id,tablename,startdate,enddate):
    persql = "select * from permission where userid='%s' and tablename='%s'"% (id,tablename)
    print(persql)
    context.permission = pd.read_sql_query(persql, dbengine)
    if len(context.permission)>0:
        p_start=context.permission['startdate'][0]
        p_enddate=context.permission['enddate'][0]
        p_totalnum=context.permission['totalnum'][0]
        p_eachnum=context.permission['eachnum'][0]
        if startdate != '':
            startdate_T = datetime.datetime.strptime(startdate, '%Y-%m-%d')
            if startdate_T >= p_start:
                startdate = startdate
            else:
                startdate = p_start.strftime("%Y-%m-%d %H:%M:%S")[:10]
        else:
            startdate = p_start.strftime("%Y-%m-%d %H:%M:%S")[:10]
        if enddate!='':
            enddate = enddate
        else:
            enddate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:10]
        if p_totalnum > p_eachnum:
            num = p_eachnum
        else:
            num = p_totalnum
        return startdate,enddate,num
    else:
        print('该账号没有此表权限！！')
        exit()

def Islogin():
    if context.userid=='':
        print('请先登录账号！！')
        exit()
