# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/7/22 15:37
# @File : creatorsettings.py
import configparser
import sys

from Gat.util.read_ini import redini
import os


def get_slash():
    if sys.platform=="win32":
        return "\\"
    else:
        return "/"


class CreatorSettings:
    @classmethod
    def __init__(cls):
        conf = configparser.ConfigParser()
        conf.read("../config/server.ini")
        cls.conf=conf

    def get_testcase_filepath(cls,projectname, filename):
        # print(os.path.join(cls.conf.get('STATIC_VARIABLE','PROJECTS_PATH'), projectname, "datafiles", filename))
        return os.path.join(cls.conf.get('STATIC_VARIABLE','PROJECTS_PATH'), projectname, "datafiles", filename)

    def get_parameter_filepath(cls,projectpath, filename):
        return projectpath+get_slash()+"datafiles"+get_slash()+filename
# if __name__ == '__main__':
#     # CreatorSettings().get_testcase_filepath('crm','demo1testcases.xml')

