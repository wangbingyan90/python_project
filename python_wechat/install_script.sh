#!/usr/bin/env bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

cp -n wechat_1_2_1_1.py /usr/local/bin/wx
cp -n wechat_1_2_1_2.py /usr/local/bin
cd /usr/local/bin/
chmod +x wx

