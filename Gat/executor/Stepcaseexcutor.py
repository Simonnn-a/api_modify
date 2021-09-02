# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/8/4 14:28
# @File : Stepcaseexcutor.py
import os

from settings import GlobalConfig
from Gat.util.methodinvoker import MethodInvoker
from Gat.util.methodtracer import MethodTracer
from Gat.util.yamlhelp import YamlHelp
from Gat.util.XMLparsehelp import XmlParseHelp
from Gat.util.stepvaluepool import StepValuePool

slash=GlobalConfig.get_slash()
class Stepcaseexcutor:
    # @MethodTracer("==============================New Testcase: ${args[-1][]}$==============================")
    def __init__(self,project_path,case_filepath,caseid):
        self.project_path = project_path
        self.case_filepath = case_filepath
        self.testcaseid = caseid

    def execute(self,cleanValue=True):
        try:
            self.execute_testcase()
        finally:
            if cleanValue:
                self.clearvaluepool()
            else:
                pass

    def clearvaluepool(self):
        stepvaluepool = StepValuePool()
        stepvaluepool.clear_all()

    def execute_testcase(self,TestCaseID=None):
        TestCaseID = TestCaseID if TestCaseID else self.testcaseid
        self.setup()
        self.execute_step(TestCaseID)
        self.teardown()

    def get_testcase(self,TestCaseID=None):
        if str(self.case_filepath).endswith("yaml"):
            testcaselist = YamlHelp(self.case_filepath).get_testcaselist4yaml()
            params_type = ""
        else:
            testcaselist = XmlParseHelp(self.case_filepath).get_testcaselist4xml()
            params_type = "@"
        testcaseid = TestCaseID if TestCaseID else self.testcaseid
        for testcase in testcaselist:
            if testcase[params_type + "ID"] == testcaseid:
                return testcase

        raise Exception("can't find testcaseID in testcasefile!!!")

    def get_teststeps(self,testcase):
        params_type=self.get_prefix()
        teststeps = testcase["TestSteps"]["Step"]
        if not isinstance(teststeps, list):
            teststeps = [teststeps]
        for teststep in teststeps:
            for key in [params_type+"StepParametersFileName", params_type+"StepPackage", params_type+"StepModule", params_type+"StepGroup"]:
                if key not in teststep:
                    try:
                        teststep[key] = testcase[key]
                    except KeyError:
                        raise Exception("%s is not exist" % key)
        return teststeps

    def get_templateSteplistByTab_type(self):
        if str(self.case_filepath).endswith("yaml"):
            data_suffix_type=YamlHelp(self.case_filepath)
        else:
            data_suffix_type=XmlParseHelp(self.case_filepath)
        return data_suffix_type

    def get_prefix(self):
        if str(self.case_filepath).endswith("yaml"):
            params_type = ""
        else:
            params_type = "@"
        return params_type

    def excute_step_with_multiple_param(self, teststeps):
        params_type=self.get_prefix()
        for teststep in teststeps:
            if params_type+"StepsTemplateID" in teststep:
                templateSteps = self.get_templateSteplistByTab_type().get_templateSteplistByTab( ID=teststep[params_type+"StepsTemplateID"])
                self.excute_step_with_multiple_param(templateSteps)
            elif params_type+"TestCaseID" in teststep:
                self.execute_testcase(teststep[params_type+"TestCaseID"])
                # self.execute_step(testcase_project_name, testcase_file_name,teststep["@TestCaseID"])
            else:
                self.call_step_method(teststep)

    @MethodTracer()
    def setup(self):
        # stepvaluepool = StepValuePool()
        setupSteps = self.get_templateSteplistByTab_type().get_templateSteplistByTab(SetUp="True")

        if setupSteps:
            self.excute_step_with_multiple_param(setupSteps)

    @MethodTracer()
    def teardown(self):
        teardownSteps = self.get_templateSteplistByTab_type().get_templateSteplistByTab(TearDown="True")
        if teardownSteps:
            self.excute_step_with_multiple_param(teardownSteps)

    @MethodTracer()
    def clearvaluepool(self):
        stepvaluepool = StepValuePool
        stepvaluepool.clear_all()

    @MethodTracer()
    def execute_step(self,TestCaseID=None):
        TestCaseID = TestCaseID if TestCaseID else self.testcaseid
        params_type = self.get_prefix()
        testcase = self.get_testcase(TestCaseID)
        if params_type+"Env" in testcase:
            GlobalConfig.ENV=testcase[params_type+"Env"]
            print("=================现在执行环境为{}".format(GlobalConfig.ENV))
        else:
            pass
        teststeps = self.get_teststeps(testcase)
        self.excute_step_with_multiple_param(teststeps)

    @MethodTracer()
    def call_step_method(self, teststep):
        params_type=self.get_prefix()
        print(params_type)
        StepParamsFileName = teststep[params_type+"StepParametersFileName"]
        StepParamsFilepath = os.path.join(self.project_path,"datafiles",StepParamsFileName)
        # print("************************全局变量**********************")
        # print(StepParamsFilepath)

        GlobalConfig.StepParameterFilePath=StepParamsFilepath
        module_name = teststep[params_type+"StepPackage"] + "." + teststep[params_type+"StepModule"]
        instance = MethodInvoker.get_instance(module_name, teststep[params_type+"StepGroup"], module_name.split('.'))
        # print(instance)
        method = MethodInvoker.get_method(instance, teststep[params_type+"StepName"])
        # print(method)
        # params=params_type+"StepParameterID"
        # print(type(params))
        # print(params)
        # print(teststep[params_type+"StepParameterID"])
        # print(type(teststep[params_type+"StepParameterID"]))
        if params_type+"StepParameterID" not in teststep:
            method()
        else:
            method(teststep[params_type+"StepParameterID"])

#
# if __name__ == '__main__':
#     Stepcaseexcutor(r'E:\api_modif\projects\demo2',r'E:\api_modif\projects\demo2\datafiles\demo1testcases.yaml',"01_crm_course_detailsuccess")\
#         .get_teststeps("01_crm_course_detailsuccess")