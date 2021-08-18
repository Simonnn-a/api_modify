# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/8/5 15:41
# @File : methodinvoker.py

class MethodInvoker:
    """
    动态调用方法
    """
    @staticmethod
    def get_instance(moudelname,classname,packagelist):
        moudel=__import__(moudelname,fromlist=packagelist)
        klass = getattr(moudel,classname)
        instance = klass
        # traceFrameMessage()
        return instance

    @staticmethod
    def get_method(instance,methodname):
        method=getattr(instance,methodname)
        return method

