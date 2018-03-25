# -*- coding:utf-8 -*-
__author__ = 'JS'
__data__ = '2018.3.23'
import requests
from bs4 import BeautifulSoup
def douyu(douyugame):
    game_list=[]
    url='HTTPs://www.douyu.com/directory/game/'+douyugame
    r = requests.get(url,verify=False)
    content=r.content
    soup = BeautifulSoup(content,"lxml")
    live_list=soup.find_all('li',attrs = {'data-cid' : True})
    for i in live_list:
        #print (i)
        try:
            all_game=i.find('a')
            #print (all_game)
            game_count=all_game.find('span',attrs = {'class' : 'dy-num fr'}).text
            #print (game_count)
            if '万' in game_count:
                game_count=float(game_count[0:-1])*10000

            if float(game_count)>8000:#过滤出直播间人数大于8000
                game_link='https://www.douyu.com'+all_game['href']
                game_title=all_game['title']
                game_picture= all_game.find('img')['data-original']
                game_nickname=all_game.find('span',attrs = {'class' : 'dy-name ellipsis fl'}).text
                game_dic={}
                game_dic['game_link']=game_link
                game_dic['game_title']=game_title
                game_dic['game_picture']=game_picture
                game_dic['game_nickname']=game_nickname
                game_dic['game_count']=game_count
                game_list.append(game_dic)

        except Exception as e:
            print (e)
    return game_list


if __name__=="__main__":
    douyugame=input('请输入要观看的频道[lol,jdqs(绝地求生),How(炉石传说),DOTA2],HDTX(荒岛特训),TVgame...........>\n')
    result=douyu(douyugame)
    for i in result:
        try:
           print (i)
        except Exception as e:
            print (e)
