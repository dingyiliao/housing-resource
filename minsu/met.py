# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# datetime: 2020-07-10 20:06

# from .template import *

from bs4 import BeautifulSoup
import os
import requests
import time

from .template import Job, save_filter

username = ''
passport = ''
query = {
    'shanghai': {
        'baoshan': 'd310113',
        'changning': 'd310105',
        'chongming': 'd310230',
        'fengxian': 'd310120',
        'hongkou': 'd310109',
        'huangpu': 'd310101',
        'jiading': 'd310114',
        'jingan': 'd310106',
        'jinshan': 'd310116',
        'minhang': 'd310112',
        'pudong': 'd310115',
        'putuo': 'd310107',
        'qingpu': 'd310118',
        'songjiang': 'd310117',
        'xuhui': 'd310104',
        'yangpu': 'd310110'
    }
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'cookie': '_lxsdk_cuid=187f4ed1285c8-0c2b63299bb44c-26031b51-144000-187f4ed1286c8; _hc.v=2e418ffc-283c-6335-5130-69c60313110f.1683441390; _ga=GA1.2.87154696.1683441391; _gid=GA1.2.1141141064.1683441391; uuid=F399A7DEA2610957B44BCEA7C60422C3BC4F380D25440CF55732B6BA7A517D75; iuuid=F399A7DEA2610957B44BCEA7C60422C3BC4F380D25440CF55732B6BA7A517D75; zgwww=e3b943a0-eca2-11ed-b2e0-89b2ac4900db; zg.userid.untrusted=1204836; token2=AgHAIq_yOooIVd1c1zWCjotQQ7RhgDTGPNX6hw3mSI7NDZS8pwM48qQePU81_8y9g8tCmQk4PE6qlwAAAAAtGAAA8GrGyz4WFIsSsNLBM9dMsFnmcn7ukPlYlmWAglZng7DZsVFUmhL1nkIRTFuMq-Jr; userid=904277814; _lxsdk=F399A7DEA2610957B44BCEA7C60422C3BC4F380D25440CF55732B6BA7A517D75; _gat_gtag_UA_113236691_1=1; XSRF-TOKEN=KPs8O1xK-263ajI7L1Z06kQlFCeMxhjgRcZc; _lxsdk_s=187f4ed10c1-c28-480-4b3%7C%7C119'
}


def get_html(url):
    print(url)
    resp = requests.get(url, headers=headers)
    headers.update(resp.cookies)
    return resp.text


class MeiTuan(Job):
    # host = 'https://minsu.meituan.com'  # old
    host = 'https://minsu.dianping.com'  # new

    def __init__(self, additional):
        """
        location: 行政区
        area: 城市
        minPrice: 最低价格
        maxPrice: 最高价格
        dateBegin: 入住日期
        dateEnd: 离开日期
        """
        super(MeiTuan, self).__init__(additional)
        self.__additional = additional

    @staticmethod
    def _get_pages(url):
        html = get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        target = soup.select(
            'div#J-ProductList ul.phx-paginator-wrapper li.page-item  a')
        try:
            page = int(target[-2].getText())
        except IndexError:
            page = 1
        return page

    def _get_url(self):
        url = self.host
        if self.__additional['area']:
            url += f'/{self.__additional["area"]}'
            # 添加行政区
            url += f"/{query['shanghai'][self.__additional['location']]}/#" \
                if self.__additional['location'] != 'unlimited' else '/#'
            # 添加筛选条件
            if self.__additional['filter']:
                ls = []
                for item in self.__additional['filter']:
                    ls.append(item)
                url += f'/?{"&".join(ls)}'
            return url
        return None

    def run_job(self):
        url_ = self._get_url().replace('#', 'pn1')
        pages = self._get_pages(url_)
        if pages == 1:
            url = url_.replace('/pn1', '')
        else:
            url = url_.replace('pn1', 'pn#')
        tags = 1
        if not os.path.exists('meituan'):
            os.makedirs('meituan')
        for index in range(1, pages + 1):
            html = get_html(url.replace('#', f'{index}'))
            soup = BeautifulSoup(html, 'html.parser')
            targets = soup.select(
                'div#J-layout div#J-ProductList div.loader__content a.product-card-container')
            # 每一页的每一个a标签
            for target in targets:
                item_url = self.host + target['href']
                item_img = target.select(
                    'figure.product-card div.product-image div.img-container img')[0]['src']
                item_title = target.select(
                    'div.product-card__title')[0].getText()
                item_price = \
                    target.select(
                        'figcaption.product-card__info div.product-card__price span.product-card__price__latest')[
                        0].getText().replace('\xa5', '')
                item = {
                    'url': item_url,
                    'img': item_img,
                    'title': item_title,
                    'price': item_price
                }
                save_filter(f'meituan/{tags}', item)
                tags += 1
            time.sleep(0.1)
