# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# datetime: 2020-07-10 20:07

import requests as req
from abc import ABC, abstractmethod
import json


__all__ = ['get_headers', 'get_html', 'Job', 'save_filter']


class Job(ABC):
    @abstractmethod
    def run_job(self):
        ...

    @abstractmethod
    def __init__(self, additional):
        """
        :param additional: the filter
        :type additional: dict
        """
        ...

    @abstractmethod
    def _get_url(self):
        ...


class District(object):
    def __init__(self, city_name, city_id, districts):
        """
        :param city_id: city's id
        :type city_id: str
        :param districts: administrative district of the city
        :type districts: list
        """
        self.name = city_name
        self.id = city_id
        self.ad_districts = districts


def get_headers():
    return {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }


def get_html(url):
    headers = get_headers()
    resp = req.get(url, headers=headers)
    return resp.text


def save_filter(file, context):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(context, f, ensure_ascii=False)
        f.flush()
