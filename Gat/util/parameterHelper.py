# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/8/6 17:02
# @File : parameterHelper.py
from Gat.util.XMLparsehelp import XmlParseHelp
from Gat.util.yamlhelp import YamlHelp
from Gat.util.stepvaluepool import StepValuePool
from Gat.util.dichelper import DictHelper
from settings import GlobalConfig


class ParameterHelper():

    @staticmethod
    def getStepParameters(parameterID):
        StepParameterFilePath=GlobalConfig.StepParameterFilePath
        print(StepParameterFilePath)
        if StepParameterFilePath.endswith("yaml"):
            stepParameters = YamlHelp(StepParameterFilePath).get_stepParameters4yaml(parameterID)
        else:
            allstr_stepParameters = XmlParseHelp(StepParameterFilePath).get_stepParameters4xml(parameterID)
            single_layer_stepParameters=DictHelper.dicVstr2num(allstr_stepParameters)
            stepParameters = DictHelper.paramstr2dic(single_layer_stepParameters)
            stepParameters = DictHelper.convert_byte2str(stepParameters)
        # traceFrameMessage("stepParameters: %s" % str(stepParameters), level="debug")
        # print("stepParameters是：                 ")
        # print(stepParameters)
        return stepParameters

    @staticmethod
    def get_selected_param(params, key):
        if key in params:
            return params[key]
        if "join_sign" in params:
            if key in params["join_sign"]:
                return params["join_sign"][key]

        valuepool = StepValuePool()
        return valuepool.get_value(key)

    @staticmethod
    def set_params(params,key,value):
        if params == None:
            params = {}
        params[key] = value

    @staticmethod
    def set_join_sign_params(params,key,value):
        if params == None:
            params = {}
        if "join_sign" not in params:
            params.setdefault("join_sign")
            params["join_sign"] = {}
        if value==None:
            return
        params["join_sign"][key] = value



