# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/7/21 14:28
# @File : yamlhelp.py
import json

import yaml
import re
class YamlHelp:
    @classmethod
    def __init__(cls,yamlfilepath):
        with open(yamlfilepath,encoding="utf-8") as yaml_file:
            data=yaml_file.read()
            data_dict=yaml.safe_load(data)
        cls.root_dict=data_dict


    def get_testcaselistdict4yaml(cls):
        test_dict=cls.root_dict['TestCaseList']
        return test_dict


    def get_testcaselist4yaml(cls):
        if "TestCase" not in cls.root_dict["TestCaseList"]:
            return None
        testcaselist = cls.root_dict["TestCaseList"]["TestCase"]
        if not isinstance(testcaselist,list):
            testcaselist = [testcaselist]
        for testcase in testcaselist:
            for key in ["StepParametersFileName", "StepPackage", "StepModule", "StepGroup"]:
                if key not in testcase:
                    try:
                        testcase[key] = cls.root_dict["TestCaseList"][key]
                    except KeyError:
                        raise  Exception("{} in not exist".format(key))
        print(testcaselist)
        return testcaselist


    def initializeStepParametersByTab(cls,stepParameters, tab):
        if tab not in stepParameters:
            stepParameters.setdefault(tab)
        if stepParameters[tab] == None:
            stepParameters[tab] = {}

    def get_stepParameters4yaml(cls, parameterID):
        # print(cls.root_dict)
        stepParameter_list = cls.root_dict["StepParametersList"]["StepParameter"]
        if not isinstance(stepParameter_list,list):
            stepParameter_list=[stepParameter_list]
        for stepParameters in stepParameter_list:
            if stepParameters["ID"] == parameterID:
                for key in ["Req_type","Rsp_type"]:
                    if key not in stepParameters:
                        try:
                            stepParameters[key] = cls.root_dict["StepParametersList"][key]
                        except KeyError as e:
                            print(e)
                cls.initializeStepParametersByTab(stepParameters, "Parameters")
                if "Expect" not in stepParameters:
                    stepParameters.setdefault("Expect")
                return stepParameters

    def get_templateSteplistByTab(cls, ID=None, SetUp=None, TearDown=None):
        if "StepsTemplate" not in cls.root_dict["TestCaseList"]:
            return None
        stepsTemplate_list = cls.root_dict["TestCaseList"]["StepsTemplate"]
        if not isinstance(stepsTemplate_list, list):
            stepsTemplate_list = [stepsTemplate_list]
        templateStep_list = None
        for stepsTemplate in stepsTemplate_list:
            try:
                if ID:
                    if stepsTemplate["ID"] == ID:
                        templateStep_list = stepsTemplate["Step"]
                if SetUp:
                    if stepsTemplate["SetUp"] == SetUp:
                        templateStep_list = stepsTemplate["Step"]
                if TearDown:
                    if stepsTemplate["TearDown"] == TearDown:
                        templateStep_list = stepsTemplate["Step"]
            except KeyError:
                pass
            if templateStep_list != None:
                if not isinstance(templateStep_list, list):
                    templateStep_list = [templateStep_list]
                for templateStep in templateStep_list:
                    for key in ["StepParametersFileName", "StepPackage", "StepModule", "StepGroup"]:
                        if key not in templateStep:
                            try:
                                templateStep[key] = cls.root_dict["TestCaseList"][key]
                            except KeyError:
                                raise Exception("{} in not exist".format(key))
                return templateStep_list
# if __name__ == '__main__':
#     # yamlfilepath = r"E:\api_modif\projects\demo\datafiles\demo1testcases.yaml"
#     # a=yamlhelp(yamlfilepath)
#     # a.get_testcaselist4yaml()
#     yamlhelp(r"E:\api_modif\projects\demo\datafiles\demo1parameters.yaml").get_stepParameters4yaml('crm_course_lesson_detailSuccess')




