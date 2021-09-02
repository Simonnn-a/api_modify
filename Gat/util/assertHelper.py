# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/8/18 10:27
# @File : assertHelper.py
from Gat.util.methodtracer import traceFrameMessage


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
        if isinstance(src_data,dict):
            if isinstance(dst_data,list):
                for dst_element in dst_data:
                    try:
                        AssertHelper.assert_dict_contain(src_data,dst_element)
                        return True
                    except Exception as e:
                        # print(e)
                        pass
                raise Exception("src_dict {} not in dst_list {}".format(src_data,dst_data))
            else:
                for key in src_data:
                    # if isinstance(dst_data, dict):
                    assert dst_data.__contains__(key)
                    AssertHelper.assert_dict_contain(src_data[key],dst_data[key])
        elif isinstance(src_data, list):
            if isinstance(dst_data, list):
                for element in src_data:
                    AssertHelper.assert_dict_contain(element, dst_data)
            else:
                raise Exception("src_data is list but dst_data is not")
        else:
            if isinstance(dst_data,list):
                assert src_data in dst_data, "value '{}' not in '{}'".format(src_data, dst_data)
            else:
                assert src_data == dst_data, "value '{}' != '{}'".format(src_data, dst_data)

    @staticmethod
    def assert_dict_contain_after_logging(src_data, dst_data):
        traceFrameMessage("Expected Result: {}".format(src_data))
        traceFrameMessage("Actual Result: {}".format(dst_data))
        return AssertHelper.assert_dict_contain(src_data, dst_data)

if __name__ == "__main__":
    xx = {"222":{"44":{"66":[{"333": 555},{"555": 666}]}}}
    yy = {"111": None,"222":{"33": 44,"44":[{"55": 66},{"66": [{"333": 444},{"333": 555},{"555": 666,"777":888}]}]}}

    exp_result = {'message': 'true', 'code': 0, 'result': {'uid': 1015893, 'id': 105, "receiverProvince": "hunan",
                                                           'receiverName': 'test'}}
    act_result = {"code": 0, "message": "true", "result": [{"id": 113, "uid": 1015893, "receiverProvince": "Beijing",
                "receiverCity": "beijing", "receiverDistrict": "chaoyang", "receiverAddress": "testAdd", "receiverMobile": "16666666666",
                "receiverName": "test"}, {"id": 112, "uid": 1015892, "receiverProvince": "hebei", "receiverCity": "beijing", "receiverDistrict": "chaoyang", "receiverAddress": "testAdd", "receiverMobile": "16666666666", "receiverName": "test"}, {"id": 111, "uid": 1015893, "receiverProvince": "Beijing", "receiverCity": "beijing", "receiverDistrict": "chaoyang", "receiverAddress": "testAdd", "receiverMobile": "16666666666", "receiverName": "test"}, {"id": 110, "uid": 1015893, "receiverProvince": "Beijing", "receiverCity": "beijing", "receiverDistrict": "chaoyang", "receiverAddress": "testAdd", "receiverMobile": "16666666666", "receiverName": "test"}, {"id": 109, "uid": 1015893, "receiverProvince": "Beijing", "receiverCity": "beijing", "receiverDistrict": "chaoyang", "receiverAddress": "testAdd", "receiverMobile": "16666666666", "receiverName": "test"}, {"id": 108, "uid": 1015893, "receiverProvince": "Beijing", "receiverCity": "beijing", "receiverDistrict": "chaoyang", "receiverAddress": "testAdd", "receiverMobile": "16666666666", "receiverName": "test"}, {"id": 107, "uid": 1015893, "receiverProvince": "Beijing", "receiverCity": "beijing", "receiverDistrict": "chaoyang", "receiverAddress": "testAdd", "receiverMobile": "16666666666", "receiverName": "test"}, {"id": 106, "uid": 1015893, "receiverProvince": "Beijing", "receiverCity": "beijing", "receiverDistrict": "chaoyang", "receiverAddress": "testAdd", "receiverMobile": "16666666666", "receiverName": "test"}, {"id": 105, "uid": 1015893, "receiverProvince": "hunan", "receiverCity": "beijing", "receiverDistrict": "chaoyang", "receiverAddress": "testAdd", "receiverMobile": "16666666666", "receiverName": "test"}]}

    # assert "1015893" in []
    xx1 = {"111": None, "23456": {"22222": 9999, "33333": "0000", "list": ["3333", "4444"]}}
    yy1 = {"111": None, "23456": {"22222": 9999, "33333": "0000", "list": ["111", "3333", "4444"]}}
    #assert_dict_contain(xx1, yy1)
    list1 = [{"333": 444},{"444": 555},{"s":"7日vip"}]

    #print(list1)

    src_dic = {'productid': 'com.ihuman.pinyin.android.cons.vip3m'}
    dst_dic = [{'productid': 'com.ihuman.pinyin.android.cons.vip1y', 'ptype':
        1, 'title': '包年VIP', 'normalPrice': {'purchaseid': 'com.ihuman.pinyin.android.cons.vip1y', 'price': 16800,
                                             'showPrice': 36000, 'platform': 3, 'discountDes': '14元/月',
                                             'supportPay': 2044}, 'supportAppversion': '1.2.1',
                'pdetail': {'timeVip': {'type': 3, 'continuous': 1, 'vmonth': 12}, 'weight': 100},
                'activityId': 'default', 'hideFlag'
                : 2}, {'productid': 'com.ihuman.pinyin.android.cons.vip3m', 'ptype': 1, 'title': '包季VIP',
                       'normalPrice': {'purchaseid': 'com.ihuman.pinyin.android.cons.vip3m', 'price':
                           6800, 'showPrice': 10800, 'platform': 3, 'discountDes': '16元/月', 'supportPay': 2044},
                       'supportAppversion': '1.0.0', 'pdetail': {'timeVip': {'type': 2, 'vmonth': 3}, "weight": 110},
                       'activityId': 'default', 'hideFlag': 2},
               {'productid': 'com.ihuman.pinyin.ncons.allpack.2', 'ptype': 2, 'title': '永久课程包', 'description': '永久课程包',
                'normalPrice': {'purchaseid': 'com.ihuman.pinyin.ncons.allpack.2', 'price': 18800, 'showPrice': 36500,
                                'platform': 3, 'supportPay': 2044}, 'supportAppversion': '1.0.0',
                'pdetail': {'weight': 90}, 'backupProductid': 'com.ihuman.pinyin.ncons.allpack.2',
                'activityId': 'default', 'hideFlag': 3}]
    # AssertHelper.assert_dict_contain_after_logging(src_dic, dst_dic)
    assert "key".__contains__("key")
    a=[{"key":"value"},"222"]
    b={"key":"value","222":"1111"}
    AssertHelper.assert_dict_contain(a, b)

