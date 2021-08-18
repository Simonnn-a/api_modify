# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/8/11 11:09
# @File : dichelper.py
from collections.abc import MutableMapping
class DictHelper:
    @staticmethod
    def str2num(str):
        str = str.encode("UTF-8")#规定字符 同时str转换成bytes
        if "\"".encode() not in str:
            try:
                num = int(str)
                return num
            except (TypeError,ValueError):
                pass
            try:
                num=float(str)
                return num
            except (TypeError,ValueError):
                pass
        else:
            str=str.replace("\"".encode(),"".encode())
        return str

    @staticmethod
    def dicVstr2num(dic):
        for k,v in dic.items():
            if v != None:
                if isinstance(v,dict):
                    v = DictHelper.dicVstr2num(v)
                else:
                    if isinstance(v,list):
                        print("++*+**++*+*++**+*+*+****+**++++*list value: {}".format(v))
                        value_list=[]
                        for ele in v:
                            if ele != None:
                                if isinstance(ele, dict):
                                    value_list.append(DictHelper.dicVstr2num(ele))
                                else:
                                    value_list.append(DictHelper.str2num(ele))
                        v=value_list
                    else:
                        v = DictHelper.str2num(v)
                dic[k]=v
        return dic

    @staticmethod
    def str2dic(key,value):
        keys = key.split(".")
        if isinstance(value,dict):
            d2={}
            for k,v in value.items():
                d1=DictHelper.str2dic(k,v)
                d2=DictHelper.rec_merge(d1,d2)
            value = d2
        if len(keys) == 1:
            return {key: value}
        else:
            return {keys[0]: DictHelper.str2dic(".".join(keys[1:]), value)}

    @staticmethod
    def rec_merge(d1,d2):
        for k,v in d1.items():
            if k in d2:
                if all(isinstance(e,list) for e in (v,d2[k])):
                    print("===============list appear")
                    for element in v:
                        d2[k].append(element)
                    continue

                if all(isinstance(e,MutableMapping) for e in (v,d2[k])):
                    d2[k] = DictHelper.rec_merge(v,d2[k])
        d3 = d1.copy()
        d3.update(d2)
        return d3

    @staticmethod
    def dict_insert_list(dic):
        """
        {"a-0":{"b":"1"}}------>{"a":[{"b":"1"}]}
        :param dic:
        :return:
        """
        for k in list(dic):
            if isinstance(dic[k],dict):
                dic[k] = DictHelper.dict_insert_list(dic[k])
            if "-" in k:
                list_key = k.split("-")[0]
                if list_key in dic:
                    dic[list_key].append(dic.pop(k))
                else:
                    dic[list_key]=[dic.pop(k)]
        return dic

    @staticmethod
    def paramstr2dic(case_data):
        dic = {}
        for key, value in case_data.items():
            d1 = DictHelper.str2dic(key,value)
            dic = DictHelper.rec_merge(d1,dic)
        dic = DictHelper.dict_insert_list(dic)
        return dic

    @staticmethod
    def params_pop_prefix(params,prefix):
        sign = None
        if prefix in params:
            sign = params.get(prefix)
            params.pop(prefix)
        if isinstance(sign,dict):
            params.update(sign)
        return params

    @staticmethod
    def convert_byte2str(data):
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        if isinstance(data, dict):
            # for key,value in data.items():
            return dict(map(DictHelper.convert_byte2str, data.items()))
        if isinstance(data, list):
            return list(map(DictHelper.convert_byte2str, data))
        if isinstance(data, tuple):
            return map(DictHelper.convert_byte2str, data)
        return data



        










