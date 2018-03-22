# -*- coding:utf-8 -*-
import requests
import re
import pymysql
import threading

class Sql(object):
    conn = pymysql.connect(host='localhost',user='root',password='root',db='test',
                     port=3306,charset='utf8')
    def addnovel(self,sort,sortname,name,imgurl,description,status,author):
        cur = self.conn.cursor()
        sql ='''INSERT INTO novel(sort,sortname,name,imgurl,description,status,author
) VALUES (%s,"%s","%s","%s","%s","%s","%s")'''
        cur.execute(sql % (sort,sortname,name,imgurl,description,status,author))
        lastrowid = cur.lastrowid
        cur.close()
        self.conn.commit()
        return lastrowid

        # cur = self.conn.cursor()
        # cur.execute('insert into novel(sort,sortname,name,imgurl,description,status,author) values ( %s,"%s","%s","%s","%s","%s","%s") %(sort,sortname,name,imgurl,description,status,author)')
        # lastrowid = cur.lastrowid
        # cur.close()
        # self.conn.commit()
        # return lastrowid

    def addchapter(self,novelid,title,content):
        # cur = self.conn.cursor()
        # sql ='''INSERT INTO chapter(novelid,title,content) VALUES(%s,"%s","%s")'''
        # cur.execute( sql % (novelid,title,content))
        # cur.close()
        # self.conn.commit()

        cur = self.conn.cursor()
        cur.execute('INSERT INTO chapter(novelid,title,content) VALUES(%s,"%s","%s")' %(novelid,title,content))
        cur.close()
        self.conn.commit()

mysql = Sql()

sort_dict = {
    '1':'玄幻魔法',
    '2':'武侠修真',
    '3':'纯爱耽美',
    '4':'都市言情',
    '5':'职场校园',
    '6':'穿越重生',
    '7':'历史军事',
    '8':'网游动漫',
    '9':'恐怖灵异',
    '10':'科幻小说',
    '11':'美文名著',
    '12':'热门推荐'}


# def getChapterContent(url,url_html,lastrowid,title):
#     html = requests.get('%s/%s' %(url,url_html)).text
#     #<script type="text/javascript">style5();</script>...........<script type="text/javascript">style6();</script>
#     #style5()后面的()是监听索引,必须转义掉
#     reg = r'style5\(\);</script>(.*?)<script type="text/javascript">style6'
#     html = re.findall(reg,html)[0]
#     mysql.addchapter(lastrowid,title,html)
# def getChapterList(url,lastrowid):
#     html = requests.get(url).text.encode('iso-8859-1').decode('gbk')
#     # <a href="6209059.html" title="第1章 君主重生，共3573字"
#     reg = r'<a (.*?)" title=".*?">(.*?)</a>'
#     chapterInfo = re.findall(reg,html)
#     for url_html,title in chapterInfo:
#         getChapterList(url,url_html)
#         break


# #多线程
# def startThread(url,lastrowid,title):
#         th = threading.Thread(target=getChapterContent,args=(url,lastrowid,title))
#         th.start()

def getChapterContent(url,lastrowid,title):
    try:
        html = requests.get(url,timeout=10).text.encode('iso-8859-1').decode('gbk')
        reg = r'style5\(\);</script>(.*?)<script type="text/javascript">style6'
        html = re.findall(reg, html, re.S)[0]
        mysql.addchapter(lastrowid, title, html)
    except:
        print('错误的网址url:'+url)
    #print(html)
def getChapterList(url,lastrowid):
    html = requests.get(url).text.encode('iso-8859-1').decode('gbk')
    #<a href="http://www.quanshuwang.com/book/135/135975/36209059.html" title="第1章 君主重生，共3573字">第1章 君主重生</a>
    reg = r'<li><a href="(.*?)" title=".*?">(.*?)</a>'
    chapterInfo = re.findall(reg,html)
    # <a href="http://www.quanshuwang.com/book/135/135975/36209059.html" title="第1章 君主重生，共3573字"
    for url,title in chapterInfo[:50]:
        getChapterContent(url, lastrowid, title)
        #print(url,title)
        #启动多线程
        # th =threading.Thread(target=getChapterContent,args=(url,lastrowid,title))
        # th.start()
def getNovel(url,sort_id,sort_name):
    html =requests.get(url).text.encode('iso-8859-1').decode('gbk')
    # print(html)
    #<meta property="og:novel:book_name" content="长生庄主">
    reg = r'<meta property="og:novel:book_name" content="(.*?)"/>'
    bookname = re.findall(reg,html)[0]
    #<meta property="og:image" content="http://www.quanshuwang.com/modules/article/images/nocover.jpg">
    reg = r'<meta property="og:image" content="(.*?)"/>'
    image = re.findall(reg,html)[0]
    reg = r'<meta property="og:description" content="(.*?)"/>'
    description = re.findall(reg,html,re.S)[0]
    # # <meta property="og:novel:category" content="玄幻魔法">
    reg = r'<meta property="og:novel:category" content="(.*?)"/>'
    category = re.findall(reg,html)[0]
    # #<meta property="og:novel:author" content="天上有飞鱼">
    reg = r'<meta property="og:novel:author" content="(.*?)"/>'
    author = re.findall(reg,html)[0]
    # #<meta property="og:novel:status" content="连载">
    reg = r'<meta property="og:novel:status" content="(.*?)"/>'
    status = re.findall(reg,html)[0]
    #<a href="http://www.quanshuwang.com/book/135/135975" class="reader"
    reg = r'<a href="(.*?)" class="reader" '
    chapterUrl = re.findall(reg,html)[0]
    # print(bookname,description,author,status,category,image,chapterUrl)

    lastrowid = mysql.addnovel(sort_id,sort_name,bookname,image,description,status,author)
    getChapterList(chapterUrl,lastrowid)
def getList(sort_id,sort_name):
    html = requests.get('http://www.quanshuwang.com/list/%s_1.html'%(sort_id)).text.encode('iso-8859-1').decode('gbk')
    # req.encoding = 'gbk'
    # content = req.text
    reg = r'<a target="_blank" href="(.*?)" class="l mr10">'
    urlList = re.findall(reg, html)
    for url in urlList:
        getNovel(url,sort_id,sort_name)

for sort_id,sort_name in sort_dict.items():
    getList(sort_id,sort_name)




