

import requests
import json


class DoubanMovie(object):
    def __init__(self):
        self.request = requests.session()

    def login_douban(self):
        login_url='https://www.douban.com/accounts/login'
        header={
            'Connection': 'keep-alive',
            'Host': 'www.douban.com',
            'Origin': 'https://www.douban.com',
            'Referer':'https://www.douban.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        data={
            'source': 'None',
            'redir': 'https://www.douban.com/',
            'form_email': '18137980325',
            'form_password': '*******',
        }
        #模拟POST douban登陆
        p = self.request.post(url=login_url,headers=header,data=data)
        print(p)
        # 利用保持的Session打开主页获取登录信息
        result=self.request.get('https://www.douban.com/').text
        #print(result)
        if '夏日似燃' in result:
            print ('恭喜,登陆douban成功')


    def douban_movie(self):
        movie_list=[]
        url='https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=100&page_start=0'
        r = self.request.get(url,verify=False)
        content=r.content
        result=json.loads(content) # https://jsonformatter.curiousconcept.com/
        tvs=result['subjects']
        for i in range (0,len(tvs)):
            tv={}
            tv['rate']=tvs[i]['rate']
            tv['cover']=tvs[i]['cover']
            tv['url']=tvs[i]['url']
            tv['title']=tvs[i]['title']
            movie_list.append(tv)
        print(movie_list)
        return movie_list

if __name__=="__main__":
    movie = DoubanMovie()
    movie.login_douban()
    movie.douban_movie()



