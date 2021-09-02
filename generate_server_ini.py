# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/7/22 16:54
# @File : generate_server_ini.py
import io
import os
import sys
from settings import GlobalConfig
# print(os.path.dirname(os.path.abspath(__file__)))

def generate_server_ini():
    slash=GlobalConfig.get_slash()
    root_dir = os.path.dirname(os.path.abspath(__file__))
    templates_path = root_dir + slash + "CaseCreator" +slash+ "templates" +slash + "server.txt"
    ini_path = root_dir + slash + "config" + slash + "server.ini"

    txtfile=open(templates_path, mode="r", encoding="utf-8")
    txtcontent=txtfile.read()
    txtcontent=txtcontent.replace('{rootdir}',root_dir)
    txtcontent=txtcontent.replace('{slash}',slash)
    txtfile.close()

    if os.path.exists(ini_path):
        os.remove(ini_path)

    serverini=open(ini_path, mode="w", encoding="utf-8")
    serverini.write(txtcontent)
    serverini.close()
if __name__ == '__main__':
    generate_server_ini()

