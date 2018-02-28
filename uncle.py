# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 01:56:40 2018

@author: ningshangyi
"""

import requests
#from bs4 import BeautifulSoup as bs
import argparse
import _thread
#import sys
import io
from PIL import Image

#num = 668357912669
R = 'b\'{"error":"Document not found"}\'' # 无对应图片的返回值
# 我在本地需要加这一句，否则会因网络问题报错，在服务器上不需要
requests.adapters.DEFAULT_RETRIES = 5

def getImg(start, length):
    print('Started %d %d' % (start, length))
    end = start + length
    num = start
    while num < end:
        num += 1
#        sys.stdout.write('%d' % num)
        try:
            url = "http://7xpsm9.com1.z0.glb.clouddn.com/f" + str(num) + "?imageslim"  
            response = requests.Session()
            # 同样只在本地需要
            response.keep_alive = False
            response = response.get(url).content
            if str(response) != R:
                print('%d with no =' % num)
                # 保存图片到当前目录， Linux系统写法， 其他系统请自行更改
                image = Image.open(io.BytesIO(response))
                image.save(str(num)+'.jpg')
    # 有的图片网址后面会有等号，原因不明，但是数量不多，所以就注释掉了
    #        url = "http://7xpsm9.com1.z0.glb.clouddn.com/f" + str(num) + "?imageslim="  
    #        response = requests.Session()
    #        response.keep_alive = False
    #        response = response.get(url).content
    #        if str(response) != R:
    #            print('%d with =' % start)
        except Exception as e:
            print(repr(e))
        if num % 10000 == 0:
            print('%d' % num)
    global lock
    lock -= 1


parser  = argparse.ArgumentParser()
# 线程数
parser.add_argument('-t', type=int, default=20)
# 每个线程的网页数量， 默认是总数/线程数
parser.add_argument('-l', type=int, default=0)
args    = parser.parse_args()
length = args.l if args.l else int(90000000000 / args.t)
start = 10000000000
lock = args.t # 用于判断子程序是否完成
for i in range(args.t):
#    sys.stdout.write('Started %d \n' % start)
    _thread.start_new_thread(getImg, (start, length))
    start += length
while lock:
    pass
