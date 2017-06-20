#! /usr/bin/env python
# -*- coding=utf-8 -*-
# @author zhangyuan
import psutil
import requests


class Watch:
    info = {}

    fpm_url = "http://127.0.0.1:8000/fpm_ping"

    nginx_url = "http://127.0.0.1:8000/nginx_status"

    post_url = ""

    # 检查时间
    def __init__(self):
        self.cpu_info()
        self.disk_info()
        self.boot_time()
        self.nginx_status()
        self.fpm_status()

    def cpu_info(self):
        self.info['cpu_logical_count'] = psutil.cpu_count()
        self.info['cpu_count'] = psutil.cpu_count(logical=False)

    def disk_info(self):
        self.info['disk_partitions'] = psutil.disk_partitions()
        self.info['disk_usage'] = psutil.disk_usage('/')

    def boot_time(self):
        self.info['boot_time'] = psutil.boot_time()

    def nginx_status(self):
        nginx = requests.get(self.nginx_url, 'timeout=1')
        self.info['nginx_ok'] = nginx.status_code == requests.codes.ok

    def fpm_status(self):
        fpm = requests.get(self.fpm_url, 'timeout=1')
        self.info['fpm_ok'] = fpm.status_code == requests.codes.ok

    def __main__(self):
        # requests.post(self.post_url, self.info, 'timeout=1')
        print self.info


if __name__ == '__main__':
    Watch().__main__()
