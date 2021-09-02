# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/7/12 16:23
# @File : xmlgenerate.py

dic={
    "path":"/course/lesson/student/ranking",
    "method":"post",
    "package":"projects.middle_platform.crm.stepgroups",
    "DESC":"根据课时查询学员完课榜"
}



def generate_test(dic):
    xmlpath=r"D:\newpro\xmlgen\datafiles"
    path = dic.get('path')
    module = "crm" + path.replace("/", "_")
    stepgroup = (path.replace("/", "")).title()
    test_xml_name = module + "testcases" + '.xml'
    para_xml_name = module + "parameters" + '.xml'
    test_template=open(r"D:\newpro\xmlgen\conf\testxml.txt", mode='r', encoding='utf-8')
    test_content= test_template.read()
    test_content = test_content.replace('{module}',module)
    test_content = test_content.replace('{group}', stepgroup)
    test_content = test_content.replace('{path}', dic["path"])
    test_content = test_content.replace('{method}', dic["method"])
    test_content = test_content.replace('{package}', dic["package"])
    test_content = test_content.replace('{para_name}', para_xml_name)
    test_content = test_content.replace('{DESC}', dic["DESC"])
    test_xml_file = open(xmlpath+'/'+test_xml_name,mode="w",encoding="utf-8")
    test_xml_file.write(test_content)
    test_xml_file.close()
def generate_para(dic):
    path = dic.get('path')
    module = "crm" + path.replace("/", "_")
    xmlpath = r"D:\newpro\xmlgen\datafiles"
    para_xml_name = module + "parameters" + '.xml'
    para_template = open(r"D:\newpro\xmlgen\conf\paraxml.txt", mode='r', encoding='utf-8')
    para_content=para_template.read()
    para_content = para_content.replace('{module}',module)
    para_xml_file = open(xmlpath+'/'+para_xml_name,mode="w",encoding="utf-8")
    para_xml_file.write(para_content)
    para_xml_file.close()

if __name__ == '__main__':
    generate_test(dic)
    generate_para(dic)