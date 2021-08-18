# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/8/4 14:28
# @File : Stepcaseexcutor.py
from CaseCreator.creatorsettings import CreatorSettings
from Gat.util.methodinvoker import MethodInvoker
from Gat.util.yamlhelp import YamlHelp
from Gat.util.XMLparsehelp import XmlParseHelp
from Gat.util.stepvaluepool import StepValuePool


class Stepcaseexcutor:
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
        # pass
        stepvaluepool = StepValuePool()
        stepvaluepool.clear_all()

    def execute_testcase(self,TestCaseID=None):
        self.setup()
        self.execute_step(TestCaseID)
        self.teardown()

    def get_teststeps(self,TestCaseID=None):
        if str(self.case_filepath).endswith("yaml"):
            testcaselist=YamlHelp(self.case_filepath).get_testcaselist4yaml()
            params_type = ""
        else:
            testcaselist =XmlParseHelp(self.case_filepath).get_testcaselist4xml()
            params_type = "@"
        testcaseid = TestCaseID if TestCaseID else self.testcaseid
        for testcase in testcaselist:
            if testcase[params_type+"ID"] == testcaseid:
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

    def excute_step_with_multiple_param(self, teststeps):
        if str(self.case_filepath).endswith("yaml"):
            params_type = ""
        else:
            params_type = "@"
        for teststep in teststeps:
            if params_type+"StepsTemplateID" in teststep:
                templateSteps = self.get_templateSteplistByTab_type().get_templateSteplistByTab( ID=teststep[params_type+"StepsTemplateID"])
                self.excute_step_with_multiple_param(templateSteps)
            elif params_type+"TestCaseID" in teststep:
                self.execute_testcase(teststep[params_type+"TestCaseID"])
                # self.execute_step(testcase_project_name, testcase_file_name,teststep["@TestCaseID"])
            else:
                self.call_step_method(teststep)


    def setup(self):
        # stepvaluepool = StepValuePool()
        TestCaseFilePath = self.case_filepath
        setupSteps = self.get_templateSteplistByTab_type().get_templateSteplistByTab(SetUp="True")

        if setupSteps:
            self.excute_step_with_multiple_param(setupSteps)

    def teardown(self):
        TestCaseFilePath = self.case_filepath
        teardownSteps = self.get_templateSteplistByTab_type().get_templateSteplistByTab(TearDown="True")
        if teardownSteps:
            self.excute_step_with_multiple_param(teardownSteps)

    # def clearvaluepool(self):
    #     # pass
    #     stepvaluepool = StepValuePool()
    #     stepvaluepool.clear_all()

    def execute_step(self,TestCaseID=None):
        TestCaseFilePath = self.case_filepath
        teststeps = self.get_teststeps(TestCaseID)
        self.excute_step_with_multiple_param(teststeps)

    def call_step_method(self, teststep):
        if str(self.case_filepath).endswith("yaml"):
            params_type = ""
        else:
            params_type = "@"
        StepParamsFileName = teststep[params_type+"StepParametersFileName"]
        StepParamsFilepath = CreatorSettings.get_parameter_filepath(self.project_path,StepParamsFileName)
        stepvaluepool=StepValuePool()
        stepvaluepool.put_value('StepParamsFilepath',StepParamsFilepath)
        module_name = teststep[params_type+"StepPackage"] + "." + teststep[params_type+"StepModule"]
        instance = MethodInvoker.get_instance(module_name, teststep[params_type+"StepGroup"], module_name.split('.'))
        method = MethodInvoker.get_method(instance, teststep[params_type+"StepName"])
        if params_type+"StepParameterID" not in teststep:
            method()
        else:
            method(teststep[params_type+"StepParameterID"])

#
# if __name__ == '__main__':
#     Stepcaseexcutor(r'E:\api_modif\projects\demo2',r'E:\api_modif\projects\demo2\datafiles\demo1testcases.yaml',"01_crm_course_detailsuccess")\
#         .get_teststeps("01_crm_course_detailsuccess")