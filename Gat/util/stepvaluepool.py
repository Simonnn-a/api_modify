# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/8/9 15:09
# @File : stepvaluepool.py
def singleton(cls,*args,**kwargs):
    instances={}
    def _singleton():
        if cls not in instances:
            instances[cls]=cls(*args,**kwargs)
        return instances[cls]
    return _singleton()

@singleton
class StepValuePool():
    """
    被单例修饰，存放关联的数据
    """
    def __init__(self):
        self.valuepool=dict()

    def put_value(self,key,value):
        self.valuepool[key]=value

    def get_value(self,key):
        result=None
        try:
            result=self.valuepool[key]
        except Exception as e:
            print(e)
        return result

    def clear_all(self):
        self.valuepool.clear()