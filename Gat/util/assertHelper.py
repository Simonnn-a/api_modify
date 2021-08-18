# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/8/18 10:27
# @File : assertHelper.py
class AssertHelper:

    @staticmethod
    def assert_dict_equal(src_data,dst_data):
        assert type(src_data) == type(dst_data),"type: '{}' != '{}'".format(type(src_data),type(dst_data))
        if isinstance(src_data,dict):
            assert len(src_data) == len(dst_data),"dict len '{}' != '{}'".format(len(src_data),len(dst_data))
            for key in src_data:
                assert key in dst_data
                AssertHelper.assert_dict_equal(dst_data[key],src_data[key])
        elif isinstance(src_data,list):
            assert len(src_data) == len(dst_data),"list len: '{}' != '{}'".format(len(src_data),len(dst_data))
            for src_list,dst_list in zip(sorted(src_data),sorted(dst_data)):
                AssertHelper.assert_dict_equal(src_list,dst_list)
        else:
            assert src_data == dst_data,"value '{}' != '{}'".format(src_data,dst_data)

    @staticmethod
    def assert_dict_contain(src_data,dst_data):
        if isinstance(src_data,dict) and isinstance(dst_data,list):
            for dst_element in dst_data:





# if __name__ == '__main__':
#     list = ["s","1","3","a"]
#     a = zip(sorted(list))
#     print(a)

