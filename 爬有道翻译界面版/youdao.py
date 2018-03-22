from tkinter import Tk,Button,Entry,Label,Text,END
import urllib.parse
import json
import time
import random
import hashlib


class Application(object):
    def __init__(self):
        self.helper = YouDao()
        self.window = Tk()
        self.window.title('知了词典')
        self.window.geometry('280x350+700+300')

        # pack , gird ,place三种方法
        self.entry = Entry(self.window)
        self.entry.place(x=10, y=10, width=200, height=25)
        self.submit = Button(self.window, text='翻译', command=self.submit)
        self.submit.place(x=220, y=10, width=50, height=25)
        self.title_label = Label(self.window, text='翻译结果')
        self.title_label.place(x=10, y=45)
        self.result_text = Text(self.window, background='#ccc')
        self.result_text.place(x=10, y=75, width=260, height=265)

    def submit(self):
        content = self.entry.get()
        result = self.helper.crawl(content)
        self.result_text.delete(1.0,END)
        self.result_text.insert(END,result)

    def run(self):
        self.window.mainloop()


class YouDao(object):
    def __init__(self):
        pass
    def crawl(self,content):
        '''
        i = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10)),
         o = n.md5("fanyideskweb" + t + i + "ebSeFb%=XZ%T[KZ)c(sy!");
        '''
        #content = input('请输入要翻译的文字>\n')
        # salt = int(time.time() * 1000) + random.randint(0, 10)
        # n = content
        # S = "fanyideskweb"
        # r = str(salt)
        # D = "ebSeFb%=XZ%T[KZ)c(sy!"
        # sign = hashlib.md5((S + n + r + D).encode('utf-8')).hexdigest()

        data = {
            'i': content,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': '1521254706626',
            'sign': 'dc4bc9326b09a4f102251cd1e69e2cd9',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION',
            # 'action':'FY_BY_REALTIME',
            'typoResult': 'false',
        }

        data = urllib.parse.urlencode(data).encode('utf-8')
        request = urllib.request.Request(
            url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=http://www.youdao.com/',
            method='POST', data=data)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')

        target = json.loads(content)
        return target['translateResult'][0][0]['tgt']




if __name__ == '__main__':
    app =Application()
    app.run()











