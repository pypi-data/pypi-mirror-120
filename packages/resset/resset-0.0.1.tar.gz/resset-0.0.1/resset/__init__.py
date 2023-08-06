# -*- coding: utf-8 -*-
import pymssql
from resset.secret import *
from sqlalchemy import *
#solr地址
# titlesolr='http://106.75.219.243:8080/solrTA/title'
contentsolr=decrypt('36L39dqK+Yw2KxA8UiV39/smikvm7emHTaip6qjuUfdYXKLukGwaNjQQ9fb8Eap2')
# chaptersolr='http://106.75.219.243:8080/solrTA/chapter'
#TXT存储路径
PATH=u'E:/RESSET/Report'

#数据库链接
dburl=decrypt('BV4L6rzB5zITUPK+IeApvrgHUR96H64NfDz92potAnbpW57Yqh+jLn8PamZrnVF04gc/Xp3rkgj3Eu1tsFXpVWTu1Qh/hLqIy80zEleQ4r4')
db=pymssql.connect(decrypt('lLe1Js/ljrvNazOwGg0qPCn6QF1aNYoGLkl0Tu1k9Uw'), decrypt('QKQ4RAXfyse0+iqLFWewYA'), decrypt('p58sxNFfd1e4l1Eu66ZonA'), decrypt('lIPA8Yl8wzzwWDf9FdQe4g'), charset='utf8')
jydburl=decrypt('BV4L6rzB5zITUPK+IeApvkXu++2pLno6nj3cXSPKyha1t+vkWeZ5VGBdNb5KpnGtVKHMl/Tq73EqPtWA5AnPIg')
engine = create_engine(jydburl, echo=False, pool_size=1000)
dbengine=create_engine(dburl, echo=False, pool_size=1000)

