# !/usr/bin/python3
# -*- coding: utf-8 -*-
# datetime: 2020-07-10 20:03

from .met import MeiTuan
import json
import os


def reading(file):
    with open(file, 'r', encoding='utf-8') as fp:
        context = json.load(fp)
    return context


def run(fi, path):
    mt = MeiTuan(fi)
    mt.run_job()

    temp_ls = []
    for file in os.listdir(path=path):
        context = reading(f'{path}/{file}')
        temp_ls.append(context)
    return temp_ls
