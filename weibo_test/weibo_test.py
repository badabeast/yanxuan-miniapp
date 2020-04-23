# -*- coding: utf-8 -*-
"""
@author: weibo.zhang
@Created on: 2019/12/19 11:52
"""

def decoratore(func):
    def log(*args,**kwargs):
        try:
            print("当前运行方法",func.__name__)
            return func(*args,**kwargs)
        except Exception as e:
            print(e)
    return log

@decoratore
def start():
   return "666"
start()