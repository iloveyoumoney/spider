# -*- coding:utf-8 -*-
__author__='JS'
__date__='2018.03.22'

from tkinter import Tk,Button,Entry,Label,Text,END
from searchWeather import SearchWeather

class Application(object):
    def __init__(self):
        self.sw = SearchWeather()
        self.window = Tk()
        self.window.title('天气查询')
        self.window.geometry('500x250+700+300')

        # pack , gird ,place三种方法
        self.entry = Entry(self.window)
        self.entry.place(x=10, y=10, width=150, height=25)
        self.submit = Button(self.window, text='翻译', command=self.submit)
        self.submit.place(x=170, y=10, width=50, height=25)
        self.title_label = Label(self.window, text='翻译结果')
        self.title_label.place(x=10, y=45)
        self.result_text = Text(self.window, background='#ccc')
        self.result_text.place(x=10, y=75, width=480, height=150)

    def submit(self):
        content = self.entry.get()
        result = self.sw.main(content)
        self.result_text.delete(1.0,END)
        self.result_text.insert(END,result)

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    app =Application()
    app.run()
