# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/7/30 16:55
# @File : TemplatesHelper.py
def HTTP_helper(test_dict,stepgroup_content,currentproject_name):

    clean_value = True
    stepgroup_content = stepgroup_content.replace('{class_name}',test_dict["StepGroup"])
    stepgroup_content = stepgroup_content.replace('{messthod_name}', test_dict["StepModule"])
    stepgroup_content = stepgroup_content.replace('{project_name}', currentproject_name)
    if 'http_method' in test_dict:
        stepgroup_content = stepgroup_content.replace('{http_method}',test_dict['http_method'])
        if test_dict['http_method'] == 'post':
            stepgroup_content = stepgroup_content.replace('{data_type}', 'json')
        else:
            stepgroup_content = stepgroup_content.replace('{data_type}', 'params')
    else:
        stepgroup_content = stepgroup_content.replace("res_txt = requests.{http_method}(self.url, json=parameters, headers=self.header)", '"xml没有提供httpmethod，请自行完成请求发送代码"')
        stepgroup_content = stepgroup_content.replace("res_dict = json.loads(res_txt.text)", '')
        stepgroup_content = stepgroup_content.replace('print("返回值 = " + str(res_dict))', '')
    if 'path' in test_dict:
        stepgroup_content = stepgroup_content.replace('{path}',test_dict['path'])
    else:
        stepgroup_content = stepgroup_content.replace('{path}','请输入api_path')
    return stepgroup_content



def protobuf_helper(test_dict,stepgroup_content,currentproject_name):
    clean_value = True
    stepgroup_content=stepgroup_content.replace('{class_name}',test_dict["StepGroup"])
    stepgroup_content = stepgroup_content.replace('{messthod_name}', test_dict["StepModule"])
    stepgroup_content = stepgroup_content.replace('{project_name}', currentproject_name)

    return stepgroup_content