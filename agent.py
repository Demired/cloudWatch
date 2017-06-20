#! /usr/bin/env python
# -*- coding=utf-8 -*-
# @author zhangyuan
import psutil
import requests
import os
import re


class Watch:
    info = {}

    fpm_ping_url = "http://127.0.0.1:8000/fpm_ping"

    nginx_status_url = "http://127.0.0.1:8000/nginx_status"

    nginx_bin_path = "/usr/local/nginx/bin/nginx"

    fpm_bin_path = "/usr/local/php/sbin/php-fpm"

    post_url = ""

    # 检查时间
    def __init__(self):
        self.cpu_info()
        self.disk_info()
        self.boot_time()
        self.nginx_status()
        self.fpm_status()
        self.php_version()
        self.nginx_version()

    def cpu_info(self):
        cpu_times_percent = psutil.cpu_times_percent()

        self.info['cpu_logical_count'] = psutil.cpu_count()
        self.info['cpu_count'] = psutil.cpu_count(logical=False)
        cpu_info = {'user': cpu_times_percent.user,
                    'nice': cpu_times_percent.nice,
                    'system': cpu_times_percent.system,
                    'idle': cpu_times_percent.idle,
                    'iowait': cpu_times_percent.iowait,
                    'irq': cpu_times_percent.irq,
                    'softirq': cpu_times_percent.softirq,
                    'steal': cpu_times_percent.steal,
                    'guest': cpu_times_percent.guest
                    }
        self.info['cpu_info'] = cpu_info

    def disk_info(self):
        self.info['disk_partitions'] = psutil.disk_partitions()
        self.info['disk_usage'] = psutil.disk_usage('/')

    def boot_time(self):
        self.info['boot_time'] = psutil.boot_time()

    def nginx_status(self):
        nginx = requests.get(self.nginx_status_url, 'timeout=1')
        self.info['nginx_ok'] = nginx.status_code == requests.codes.ok

    def fpm_status(self):
        fpm = requests.get(self.fpm_ping_url, 'timeout=1')
        self.info['fpm_ok'] = fpm.status_code == requests.codes.ok

    def nginx_version(self):
        cmd = self.nginx_bin_path + " -v 2>&1|awk -F':' '{print $2}'|awk -F'/' '{print $2}'"
        self.info['nginx_version'] = os.popen(cmd).readlines()[0].strip()

    def php_version(self):
        cmd = self.fpm_bin_path + " -v"
        tmp = os.popen(cmd).readline()
        self.info['php_version'] = re.findall('\d\.\d\.\d{,2}', tmp)[0]

    def memory_info(self):
        virtual_memory = psutil.virtual_memory()
        memory = {'used': str(int(virtual_memory.used / 1024 / 1024)) + "M",
                  'total': str(int(virtual_memory.total / 1024 / 1024)) + "M",
                  'free': str(int(virtual_memory.free / 1024 / 1024)) + "M"}
        self.info['memory'] = memory

    def __main__(self):
        # requests.post(self.post_url, self.info, 'timeout=1')
        print self.info


if __name__ == '__main__':
    Watch().__main__()
