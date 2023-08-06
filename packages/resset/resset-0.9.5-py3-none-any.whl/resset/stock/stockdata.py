from resset.login import *
# 创建数据库交互
metadata = MetaData(engine)  # 实例化数据库对象
# dbTable = Table('literature_copy', metadata, autoload=True)

#获取股票内部代码
def get_InnerCode(security):
    code=security.split('_')[1]
    market=security.split('_')[0]
    sql="select InnerCode from SecuMain where SecuCode='%s' and SecuMarket='%s'"%(code,market)
    table=pd.read_sql_query(sql, engine)
    inner=''
    if len(table)>0:
        inner=table['InnerCode'][0]
    return inner

def get_Factor(security,date,fq):
    pass
    # try:
    #     if fq=='qfq':
    #     if len(inner) > 0:
    #         fember=session1.query(Factor).filter(Factor.InnerCode==inner[0].InnerCode).order_by(Factor.ExDiviDate.desc()).first()
    #         member=session1.query(Factor).filter(Factor.InnerCode==inner[0].InnerCode,Factor.ExDiviDate<=date).order_by(Factor.ExDiviDate.desc()).first()
    #         if member is not None:
    #             a=member.RatioAdjustingFactor
    #             b=fember.RatioAdjustingFactor
    #         else:
    #             a=1
    #             b=1
    # except:
    #     a=1
    #     b=1
    # return decimal.Decimal(str(a/b))

#A股日行情数据API
def get_history_data(security,startdate='',enddate='',fq='bfq'):
    print(context.userid)
    #判断是否登陆
    # Islogin()
    #判断账户权限
    startdate,enddate,num=query_permission(context.userid,'QT_DailyQuote',startdate,enddate)
    #获取股票内部编码
    innercode = []
    for x in security.split(','):
        inner = get_InnerCode(x)
        if inner != '':
            innercode.append(str(inner))
    innercode=str(innercode).replace('[','(').replace(']',')')
    #获取复权因子
    if fq=='bfq':
        pass
    datasql="select top %s * from QT_DailyQuote where innercode in %s and TradingDay>='%s' and TradingDay<='%s' order by InnerCode,TradingDay desc"%(str(num),innercode,startdate,enddate)
    print(datasql)
    table = pd.read_sql_query(datasql, engine)
    print(table)






if __name__ == '__main__':
    thsLogin = ressetLogin("zhangq", "123")
    get_history_data('83_600519,90_000001')
            

