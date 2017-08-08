# CloudWatch

## 软件介绍

用于监测vps的运行状态，nginx，fpm进程的起停状态，硬盘使用率，端口开关情况 等

## 设计目标

自动上传日志，清理硬盘，识别恶意ip，报告恶意ip，优化进程，生成报表，邮件提醒

## 开发背景

本大王手里有好几百个vps，每天早上起床就要扫一遍，重复的劳动就要交给机器去做

## 环境配置

```shell
wget https://bootstrap.pypa.io/get-pip.py

python get-pip.py

yum install python-devel

pip install psutil,requests
```


# 项目终止，换go去写了

