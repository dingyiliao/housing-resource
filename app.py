# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# datetime: 2020-07-10 19:41

from flask import Flask, render_template, request, make_response
from minsu import search
import random
import os
import shutil
import datetime

APPLICATION = Flask(__name__)
'''
RESOURCES = ['deviantart.svg', 'favicon.ico',
             'bing.lylares.com-2020-06-11-1080p.jpg']
'''

_RESULTS = None
KEY = None


@APPLICATION.route('/submit', methods=['get'])
def submit():
    global _RESULTS, KEY
    data = dict(request.values)
    temp_ls = []

    # 筛选附加条件
    for item in data:
        if item != 'area' and item != 'location':
            if item == 'maxPrice':
                data[item] = int(data[item]) * 100
                temp_ls.append('minPrice=0')
            temp_ls.append(f'{item}={data[item]}')

    if len(temp_ls) == 0:
        temp_ls = None

    fi = {
        'area': data['area'],
        'location': data['location'],
        'filter': temp_ls
    }
    if os.path.exists('./meituan'):  # 删除之前的缓存
        # delete specific director and it's subfiles
        shutil.rmtree('./meituan')
    # 获取文件解析结果
    path = os.path.abspath(os.curdir) + '\\meituan'
    _RESULTS = search.run(fi, path)  # 获取整理好的结果
    KEY = random.randint(0, 1000)  # 获取一个随机数以返回给客户端
    resp = {
        'code': 200,
        'key': KEY,
        'dataNum': len(_RESULTS)
    }
    print(resp)
    return make_response(resp)


# 使用一个单独的页面来展示搜索结果
@APPLICATION.route('/result/<int:_key>', methods=['get'])
def result(_key):
    resp = render_template('searching_result.html',
                           result=_RESULTS) if _key == KEY and request.referrer else f'Your ip addr: {request.remote_addr}.'
    return resp


@APPLICATION.route('/home')
@APPLICATION.route('/')
def index():
    return render_template('index.html')


@APPLICATION.before_request
def interceptor():
    # 筛选资源请求
    # for item in RESOURCES:
    #     if item in request.url:
    #         return

    # 写入日志
    # Append new access messages into thie file
    # with open('access_log.log', 'a') as fp:
    #     fp.writelines(
    #         f'********************\n'
    #         f'date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
    #         f'ip addr: ({request.remote_addr})\n'
    #         f'access url: ({request.url})\n'
    #         f'referrer: ({request.referrer})\n'
    #         f'********************\n')
    #     fp.flush()
    return


if __name__ == '__main__':
    APPLICATION.run(host='0.0.0.0', port=5000, debug=True)
