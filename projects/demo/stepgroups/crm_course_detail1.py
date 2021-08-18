    # -*- coding=utf-8 -*-
"""
crm_course_detail1success运行期望成功的case
crm_course_detail1faild运行期望失败的case
crm_course_detail1_api_relevance运行接口关联的case（需要手动修改需要存入/取出的字段值）

self.url需要自行补充！！！！！！
是否传入header根据需求决定
其他参数可以根据需求修改

"""
import allure
import json
import requests
from Gat.util.assertHelper import AssertHelper
from projects.demo import config
from Gat.util.stepvaluepool import StepValuePool
from Gat.util.parameterHelper import ParameterHelper
from Gat.util.randomdataHelper import random_phone
class Coursedetail():
    def __init__(self):
        self.url=config.URL+'/course/detail'
        self.header = config.header
    def crm_course_detail1Success(self,parameterID):
        stepParameters = ParameterHelper.getStepParameters(parameterID)
        parameters = stepParameters['Parameters']
        expect_result = stepParameters['Expect']
        #if expect_result == None:
        #    expect_result = {'code': 0}
        res_txt = requests.post(self.url, json=parameters, headers=self.header)
        res_dict = json.loads(res_txt.text)
        print("返回值 = " + str(res_dict))
        #valuepool=StepValuePool()
        #valuepool.put_value('appId',parameters['appId'])
        #valuepool.put_value('userId',parameters['userId'])
        AssertHelper.assert_dict_contain_after_logging(expect_result, res_dict)
    def crm_course_detail1Faild(self,parameterID):
        stepParameters = ParameterHelper.getStepParameters(parameterID)
        parameters = stepParameters['Parameters']
        print('Params: {}'.format(parameters))
        expect_result = stepParameters['Expect']
        #if expect_result == None:
        #    expect_result = {'code': -1}
        res_txt = requests.post(self.url, json=parameters, headers=self.header)
        res_dict = json.loads(res_txt.text)
        print("返回值 = " + str(res_dict))
        AssertHelper.assert_dict_contain_after_logging(expect_result, res_dict)
    def crm_course_detail1_Api_relevance(self,parameterID):
        stepParameters = ParameterHelper.getStepParameters(parameterID)
        parameters = stepParameters['Parameters']
        #parameters["appId"] = ParameterHelper.get_selected_param(parameters,"appId")
        #parameters["userId"] =ParameterHelper.get_selected_param(parameters,"userId")
        expect_result = stepParameters['Expect']
        #if expect_result == None:
        #    expect_result = {'code': 0}
        res_txt = requests.post(self.url, json=parameters, headers=self.header)
        res_dict = json.loads(res_txt.text)
        print("返回值 = " + str(res_dict))
        #valuepool=StepValuePool()
        #valuepool.put_value('appId',parameters['appId'])
        #valuepool.put_value('userId',parameters['userId'])
        AssertHelper.assert_dict_contain_after_logging(expect_result, res_dict)

