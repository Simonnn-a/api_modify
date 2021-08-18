#coding=utf-8
'''
Created on 2020-06-24

@author: gat runner
'''
import sys
sys.path.append(r'E:\api_modif')
import pytest
import allure
from Gat.executor.Stepcaseexcutor import Stepcaseexcutor
from Gat.util.classtracer import ClassMsgTracer

@ClassMsgTracer(r"==========Test start==========")
class Testdemo2():
    project_path = r'E:\api_modif\projects\demo2'
    case_filepath = r'E:\api_modif\projects\demo2\datafiles\demo2testcases.yaml'

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    pytest.main(['-s', '-q', 'test_demo2.py'])