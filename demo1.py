# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/8/11 11:37
# @File : demo1.py
import json

import xmltodict

with open(r"E:\api_modif\aaa.xml", encoding="utf-8") as xml_file:
    data_raw = xmltodict.parse(xml_file.read())
    xml_file.close()
    print(data_raw)
    json_str = json.dumps(data_raw)
    print(json_str)
    data_dict = json.loads(json_str)
print(data_dict)
list1=list(data_dict)
print(list1)

for k in list(data_dict):
    print(k)

def dict_insert_list(dic):
    '''
    :description:将字典中带[]的字段转化为list
    :param dic:原本的带key中带[]标记的无list字典
    :return:转化后的带list的字典
    '''
    for k in list(dic):
        # print("="*10),k,("="*10)

        if isinstance(dic[k], dict):
            dic[k] = dict_insert_list(dic[k])
        # if "[" in k:
        #     list_key = k.split("[")[0]
        if "-" in k:
            list_key = k.split("-")[0]

            if list_key in dic:
                dic[list_key].append(dic.pop(k))
                # print("%s existed in dic" % list_key)
                # print("now dic[%s]: " % list_key),dic[list_key]
            else:
                dic[list_key] = [dic.pop(k)]
                # print("%s is new in dic" % list_key)
                # print("now dic[%s]: " % list_key),dic[list_key]
    return dic
def dict_insert_list2(dic):
    key_list = list(dic.keys())
    for k in key_list:
        if "-" in k:
            list_key = k.split("-")[0]
            if list_key in dic:
                dic[list_key].append(dic.pop(k))
            else:
                dic[list_key] = [dic.pop(k)]
    return dic
dic=dict_insert_list2(data_dict)
print(dic)