# _*_ conding:utf-8 _*-
# @Author : jzy
# @Time :  2021/7/22 14:28
# @File : read_ini.py
import configparser
def redini(path,section,option):
    conf = configparser.ConfigParser()
    conf.read(path)
    value = conf.get(section,option)
    return value
