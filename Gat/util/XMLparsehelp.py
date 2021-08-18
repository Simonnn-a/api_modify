#coding=utf-8
'''
Created on 2020-06-24

@author: 张印
'''
import json
import xmltodict
# from Gat.util.dichelper import DictHelper


# open the input xml file and read
# data in form of python dictionary
# using xmltodict module

class XmlParseHelp:
    @classmethod
    def __init__(cls, xmlfilepath):
        with open(xmlfilepath,encoding="utf-8") as xml_file:
            data_raw = xmltodict.parse(xml_file.read())
            xml_file.close()
        json_str = json.dumps(data_raw)
        data_dict = json.loads(json_str)
        cls.root_dict=data_dict

    def get_testcaselistdict4xml(cls):
        test_dict = cls.root_dict['TestCaseList']
        return test_dict


    def get_testcaselist4xml(cls):
        if "TestCase" not in cls.root_dict["TestCaseList"]:
            return None
        testcaselist = cls.root_dict["TestCaseList"]["TestCase"]
        if not isinstance(testcaselist,list):
            testcaselist = [testcaselist]
        for testcase in testcaselist:
            for key in ["@StepParametersFileName", "@StepPackage", "@StepModule", "@StepGroup"]:
                if key not in testcase:
                    try:
                        testcase[key] = cls.root_dict["TestCaseList"][key.split("@")[1]]
                    except KeyError:
                        raise  Exception("%s in not exist" %key)
        print(testcaselist)
        return testcaselist

    def get_stepParameters4xml(cls,parameterID):
        stepParameter_list = cls.root_dict["StepParametersList"]["StepParameter"]
        print(stepParameter_list)
        if not isinstance(stepParameter_list, list):
            stepParameter_list = [stepParameter_list]
        for stepParameters in stepParameter_list:
            print(stepParameters)
            if stepParameters["@ID"] == parameterID:
                #stepParameters = DictHelper.dicVstr2int(stepParameters)
                for key in ["Req_type","Rsp_type"]:
                    if key not in stepParameters:
                        try:
                            stepParameters[key] = cls.root_dict["StepParametersList"][key]
                        except KeyError:
                            pass
                cls.initializeStepParametersByTab(stepParameters,"Parameters")
                if "Expect" not in stepParameters:
                    stepParameters.setdefault("Expect")
                print(stepParameters)
                return stepParameters

    def  initializeStepParametersByTab(cls,stepParameters,tab):
        if tab not in stepParameters:
            stepParameters.setdefault(tab)
        if stepParameters[tab] == None:
            stepParameters[tab] = {}

    def get_templateSteplistByTab(cls, ID=None, SetUp=None, TearDown=None):
        if "StepsTemplate" not in cls.root_dict["TestCaseList"]:
            return None
        stepsTemplate_list = cls.root_dict["TestCaseList"]["TestCaseList"]["StepsTemplate"]
        if not isinstance(stepsTemplate_list, list):
            stepsTemplate_list = [stepsTemplate_list]
        templateStep_list = None
        for stepsTemplate in stepsTemplate_list:
            try:
                if ID:
                    if stepsTemplate["@ID"] == ID:
                        templateStep_list = stepsTemplate["Step"]
                if SetUp:
                    if stepsTemplate["@SetUp"] == SetUp:
                        templateStep_list = stepsTemplate["Step"]
                if TearDown:
                    if stepsTemplate["@TearDown"] == TearDown:
                        templateStep_list = stepsTemplate["Step"]
            except KeyError:
                pass
            if templateStep_list != None:
                if not isinstance(templateStep_list,list):
                    templateStep_list=[templateStep_list]
                for templateStep in templateStep_list:
                    for key in ["@StepParametersFileName", "@StepPackage", "@StepModule", "@StepGroup"]:
                        if key not in templateStep:
                            try:
                                templateStep[key] = cls.root_dict["TestCaseList"]["TestCaseList"][key.split("@")[1]]
                            except KeyError:
                                raise Exception("%s in not exist" % key)
                return templateStep_list

# def convert_byte2str(data):
#     if isinstance(data, bytes):
#         return data.decode('ascii')
#     if isinstance(data, dict):
#         return dict(map(convert_byte2str, data.items()))
#     if isinstance(data, tuple):
#         return map(convert_byte2str, data)
#     return data

# if __name__ == "__main__":
#     # get_testcaselist4xml(r"D:\autotest\api_automation\api_pygat\projects\middle_platform\crm\datafiles\crm_course_detailtestcases.xml")
#     # get_templateSteplistByTab("test_getAgentInfocases.xml", "login-out")
#     get_stepParameters4xml(r"D:\autotest\api_automation\api_pygat\projects\middle_platform\crm\datafiles\crm_course_detailparameters.xml","crm_course_detailSuccess")