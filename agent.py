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
        self.memory_info()
        self.nginx_status()
        self.fpm_status()
        self.php_version()
        self.nginx_version()

    def cpu_info(self):
        cpu_times_percent = psutil.cpu_times_percent()
        self.info['cpu_logical_count'] = psutil.cpu_count()
        self.info['cpu_count'] = psutil.cpu_count(logical=False)
        self.info['user'] = cpu_times_percent.user
        self.info['nice'] = cpu_times_percent.nice
        self.info['system'] = cpu_times_percent.system
        self.info['idle'] = cpu_times_percent.idle

    def disk_info(self):
        disk_partitions = psutil.disk_partitions()
        disk_info = {}
        for disk in disk_partitions:
            tmp_disk_usage = psutil.disk_usage(disk.mountpoint)
            disk_info[disk.mountpoint] = {'total': tmp_disk_usage.total,
                                          'used': tmp_disk_usage.used,
                                          'percent': tmp_disk_usage.percent,
                                          'fstype': disk.fstype}
        self.info['disk'] = disk_info

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
        memory = {'used': virtual_memory.used,
                  'total': virtual_memory.total,
                  'free': virtual_memory.free}
        self.info['memory'] = memory

    def __main__(self):
        # requests.post(self.post_url, self.info, 'timeout=5')
        print self.info


if __name__ == '__main__':
    Watch().__main__()
