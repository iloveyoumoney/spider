# -*- coding:utf-8 -*-
__author__ = 'JS'
__data__ = '2018.3.23'
import requests
from bs4 import BeautifulSoup
import json
def login_51cto():
    s=requests.Session()
    #login_url = 'http://home.51cto.com/index'
    login_url='http://home.51cto.com/index'
    # content  =s.get('https://home.51cto.com/index',verify=False).content
    content=s.get(login_url).content
    #获取csrf token
    soup = BeautifulSoup(content,"lxml")
    token=soup.find('meta',attrs = {'name' : 'csrf-token'})['content']
    print (token)
    header={
        'Connection': 'keep-alive',
        'Host': 'home.51cto.com',
        'Origin': 'http://home.51cto.com',
        'Referer':'http://home.51cto.com/index',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    data={
        '_csrf':token,
        'LoginForm[username]':'295148018@qq.com',
         'LoginForm[password]': '*******',
        'LoginForm[rememberMe]': '0',
        'login-button': '登 录'
    }
    #模拟POST 51cto 登陆
    s.post(url=login_url,headers=header,data=data)
    # 利用保持的Session打开主页获取登录信息
    result=s.get('http://home.51cto.com/home').text
    #print(result)
    if '夏日似燃' in result:
        print ('恭喜,登陆51cto成功,领取下载豆中..')
    #利用保持的Session领取下载豆
    #download=s.post('http://down.51cto.com/download.php?do=getfreecredits&t=0.8367867217711695').text
    download = s.post('http://home.51cto.com/home/ajax-to-sign',headers=header,data={'_csrf':token}).text
    #download = json.loads(download)
    # if '2' in download.split(',')[1]:
    #     print ('领取成功,当前下载豆:'+ download.split(',')[0])
    # elif '1' in download.split(',')[0]:
    #     print (download)
    #     print ('抱歉,今天已经领取,请明天再来,当前下载豆:'+download.split(',')[1])
    # else:
    #     print ('请注意,领取失败')
    #print (download)

if __name__=="__main__":
    login_51cto()

