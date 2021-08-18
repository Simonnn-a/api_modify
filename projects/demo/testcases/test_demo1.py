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
class Testdemo1():
    project_path = r'E:\api_modif\projects\demo'
    case_filepath = r'E:\api_modif\projects\demo\datafiles\demo1testcases.yaml'
    @pytest.mark.P1
    def test_01_crm_course_detailsuccess(self, cleanValue=True):
        executor=Stepcaseexcutor(self.project_path, self.case_filepath, "01_crm_course_detailsuccess")
        executor.execute(cleanValue)
        
    
        
    @pytest.mark.P1
    def test_loginSuc(self, cleanValue=True):
        executor=Stepcaseexcutor(self.project_path, self.case_filepath, "loginSuc")
        executor.execute(cleanValue)
        
    
        

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    pytest.main(['-s', '-q', 'test_demo1.py'])