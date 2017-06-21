#! /usr/bin/env python
# -*- coding=utf-8 -*-
# @author zhangyuan
import psutil
import requests
import os
import re
# import time


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
                    }
        self.info['cpu_info'] = cpu_info

    def disk_info(self):
        disk_partitions = psutil.disk_partitions()

        disk_info = {}
        for disk in disk_partitions:
            tmp_disk_usage = psutil.disk_usage(disk.mountpoint)

            if tmp_disk_usage.total/1024/1024/1024 > 0:
                disk_total = str(int(tmp_disk_usage.total / 1024 / 1024 / 1024)) + "G"
            else:
                disk_total = str(int(tmp_disk_usage.total / 1024 / 1024)) + "M"

            if tmp_disk_usage.used/1024/1024/1024 > 0:
                disk_usage = str(int(tmp_disk_usage.used / 1024 / 1024 / 1024)) + "G"
            else:
                disk_usage = str(int(tmp_disk_usage.used / 1024 / 1024)) + "M"

            disk_info[disk.mountpoint] = {'total': disk_total,
                                          'used': disk_usage,
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
        memory = {'used': str(int(virtual_memory.used / 1024 / 1024)) + "M",
                  'total': str(int(virtual_memory.total / 1024 / 1024)) + "M",
                  'free': str(int(virtual_memory.free / 1024 / 1024)) + "M"}
        self.info['memory'] = memory

    def __main__(self):
        # requests.post(self.post_url, self.info, 'timeout=5')
        print self.info


if __name__ == '__main__':
    # while 1:
    Watch().__main__()
    # time.sleep(60*10)
