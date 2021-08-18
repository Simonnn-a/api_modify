# -*- coding=utf-8 -*-
# @Author : jzy
# @Time :  2021/7/22 18:28
# @File : caseCreator.py
import configparser
import os
import pathlib
import re
import shutil

from CaseCreator.creatorsettings import CreatorSettings,get_slash
from Gat.util.XMLparsehelp import XmlParseHelp
from Gat.util.yamlhelp import YamlHelp
from ihuman_common import TemplatesHelper

dir_slash=get_slash()
init_py_file_name = "__init__.py"
class Casecreator:
    @classmethod
    def __init__(cls):
        conf = configparser.ConfigParser()
        conf.read("../config/server.ini")
        cls.conf = conf

    def get_projectpath_list(cls):
        projectpath_list = []
        for subdir in os.listdir(cls.conf.get('STATIC_VARIABLE','PROJECTS_PATH')):
            if subdir != ".pytest_cache":
                # print("***dir: {}".format(subdir))
                sub_dir_path = cls.conf.get('STATIC_VARIABLE','PROJECTS_PATH') + dir_slash + subdir
                if os.path.isdir(sub_dir_path):
                    print("sub_dir_path: {}".format(sub_dir_path))
                    project_package_init_file = open(sub_dir_path + dir_slash + init_py_file_name, "w")
                    project_package_init_file.close()
                    if os.path.exists(sub_dir_path + dir_slash + "datafiles"):
                        projectpath_list.append(sub_dir_path)
                    else:
                        for subdir in os.listdir(sub_dir_path):#针对二层级目录的情况
                            subprojectpath = sub_dir_path + dir_slash + subdir
                            if os.path.isdir(subprojectpath):
                                if os.path.exists(subprojectpath + dir_slash + "datafiles"):
                                    projectname = sub_dir_path + dir_slash + subdir
                                    subproject_package_init_file = open(
                                        subprojectpath + dir_slash + init_py_file_name,
                                        "w")
                                    subproject_package_init_file.close()
                                    projectpath_list.append(projectname)
        print(projectpath_list)
        return projectpath_list

    def create_testproject(cls,project_path):
        testcases_path = project_path + dir_slash + "testcases"
        # logtmp_folder = project_path + dir_slash + "logtmp"
        project_log_path = project_path + dir_slash + "log"
        # testcases_log_path = testcases_path + dir_slash + "log"
        stepgroup_path = project_path + dir_slash + 'stepgroups'
        if os.path.exists(testcases_path):
            shutil.rmtree(testcases_path)
        os.makedirs(testcases_path)
        if os.path.exists(stepgroup_path):  # 如果目录存在
            print('stepgroups目录已存在，跳过生成步骤')
            pass
        else:
            os.makedirs(stepgroup_path)  # 创建目录
            stepgroup_path_init_file = open(stepgroup_path + dir_slash + init_py_file_name, "w")
            stepgroup_path_init_file.close()
        if not os.path.exists(project_log_path):
            os.makedirs(project_log_path)
        testcases_package_init_file = open(testcases_path+dir_slash+init_py_file_name,"w")
        testcases_package_init_file.close()
    # def get_suffix(cls,datafiles_path):
    #     global suffix
    #     for datafile in os.listdir(datafiles_path):
    #         if datafile.endswith(".xml"):
    #             suffix = ".xml"
    #         elif datafile.endswith(".yaml"):
    #             suffix = ".yaml"
    #         return suffix

    def fuzzyfinder(cls,user_input, collection):
        suggestions = []
        pattern = ''.join(user_input)  # Converts 'djm' to 'd.*j.*m'
        regex = re.compile(pattern)  # Compiles a regex.
        for item in collection:
            match = regex.search(item)  # Checks if the current item matches the regex.
            if match:
                suggestions.append((match.start(), item))
        return [x for _, x in sorted(suggestions)]

    def generate_testcase(cls,project_path):
        global suffix
        projectname = project_path.replace(cls.conf.get('STATIC_VARIABLE','PROJECTS_PATH') + dir_slash, "")
        # project_path = project_path
        testcases_path = project_path + dir_slash + "testcases"
        datafiles_path = project_path + dir_slash + "datafiles"
        xml_report_path = project_path + dir_slash + "report" + dir_slash + "xml"
        datafiles_list=os.listdir(datafiles_path)
        print(datafiles_list)
        case_list=cls.fuzzyfinder("case.",datafiles_list)
        print(case_list)
        # suffix=cls.get_suffix(datafiles_path)
        # print(suffix)
        # datafile_suffix=str("cases"+suffix)
        # testcase_suffix=str("testcases"+suffix)
        for datafile in case_list:
            print(datafile)
            # if datafile.endswith("cases"+suffix):
            if datafile.endswith("cases.xml"):
                suffix = ".xml"
                current_datafile_path=datafiles_path + dir_slash + datafile
                testcaselist = XmlParseHelp(current_datafile_path).get_testcaselist4xml()
            else:
                suffix = ".yaml"
                current_datafile_path = datafiles_path + dir_slash + datafile
                testcaselist = YamlHelp(current_datafile_path).get_testcaselist4yaml()
            datafile_suffix=str("cases"+suffix)
            testcase_suffix=str("testcases"+suffix)
            print("Get cases"+suffix+ "file: {}".format(datafile))
            # if datafile.endswith("cases.xml"):
            #     testcaselist = get_testcaselist4xml(datafiles_path + dir_slash + datafile)
            # else:
            #     testcaselist = YamlHelp(datafiles_path + dir_slash + datafile).get_testcaselist4yaml()
            print(testcaselist)
            testmethodcontent = ""
            if testcaselist:
                for testcase in testcaselist:
                    testmethodcontent = testmethodcontent + cls.create_testmethod_content(testcase) + "\n"
            if "testcases"+suffix not in datafile:
                classname_content = str(datafile.split(datafile_suffix)[0]).replace("test_", "Test")
                py_filename = str(datafile.split(".")[0]) + ".py"
            else:
                test_collection_name = str(datafile.split(testcase_suffix)[0]).rstrip("_")
                classname_content = "Test" + test_collection_name
                py_filename = "test_" + test_collection_name + ".py"
            testclass_content = cls.create_testclass_content(cls.conf.get('STATIC_VARIABLE','ROOTDIR'), classname_content, project_path, current_datafile_path,
                                                         testmethodcontent, py_filename)
            testcasefile = open(testcases_path + dir_slash + py_filename, mode="w", encoding="utf-8")
            testcasefile.write(testclass_content)
            testcasefile.close()
        runpy_content = cls.create_runpy_content(cls.conf.get('STATIC_VARIABLE','ROOTDIR'), xml_report_path)
        runpyfile = open(project_path + dir_slash + "run.py", mode="w", encoding="utf-8")
        runpyfile.write(runpy_content)
        runpyfile.close()

    def create_global_runpy(cls):
        global_report_xml_path = os.path.join(cls.conf.get('STATIC_VARIABLE','REPORT_PATH'), "xml")
        runpy_content = cls.create_runpy_content(cls.conf.get('STATIC_VARIABLE','ROOTDIR'), global_report_xml_path)
        runpyfile = open(cls.conf.get('STATIC_VARIABLE','ROOTDIR') + dir_slash + "run.py", mode="w", encoding="utf-8")
        runpyfile.write(runpy_content)
        runpyfile.close()

    def create_config_content(cls):
        config_template = open(cls.conf.get('STATIC_VARIABLE','CONG_PROJECT_TEMPLATE_PATH'), mode='r', encoding="utf-8")
        config_content = config_template.read()
        config_template.close()
        return config_content

    def create_stepgroups_content(cls,test_dict, currentproject_path):
        currentproject_name = currentproject_path.split(dir_slash + 'projects' + dir_slash)[1].replace(dir_slash, '.')
        # print("*****************{}".format(currentproject_name))
        proto_project_path = currentproject_path+dir_slash+'proto'
        proto_path = pathlib.Path(proto_project_path)
        if proto_path.exists() == True:
            stepgroup_type='STEPGROUP_PROTO_TEMPLATE_PATH'
            stepgroup_method=TemplatesHelper.protobuf_helper
        else:
            stepgroup_type='STEPGROUP_TEMPLATE_PATH'
            stepgroup_method = TemplatesHelper.HTTP_helper
        stepgroup_template = open(cls.conf.get('STATIC_VARIABLE',stepgroup_type), mode='r', encoding="utf-8")
        stepgroup_content = stepgroup_template.read()
        stepgroup_content = stepgroup_method(test_dict, stepgroup_content, currentproject_name)
        stepgroup_template.close()
        return stepgroup_content

    def set_py_filename(cls,test_dict):
        py_filename = test_dict["StepModule"]
        return py_filename

    def create_testmethod_content(cls,testcase):
        global params_type
        testmethod_template = open(cls.conf.get('STATIC_VARIABLE','TEST_METHOD_PATH'),mode='r',encoding='utf-8')
        testmethod_content = testmethod_template.read()
        pytest_mark_content = ""
        allure_desc_content = ""
        clean_value = True
        print(testcase)
        testcase_params_list = list(testcase.keys())
        print(testcase_params_list)
        xml_params=["@CaseTag","@Order","@CleanValue"]
        yaml_params=["CaseTag","Order","CleanValue"]
        if set(testcase_params_list) & set(xml_params):
            params_type = "@"
        elif set(testcase_params_list) & set(yaml_params):
            params_type = ""
        CaseTag=params_type+"CaseTag"
        Order=params_type+"Order"
        CleanValue=params_type+"CleanValue"
        if CaseTag in testcase:
            taglist = str(testcase[CaseTag]).split('+')
            for tag in taglist:
                pytest_mark_content += "    @pytest.mark." + tag + "\n"
        if Order in testcase:
            pytest_mark_content += "    @pytest.mark.run(order=" + testcase[Order] + ")" + "\n"
        if CleanValue in testcase:
            clean_value = testcase[CleanValue]
        if "Desc" in testcase:
            allure_desc_content = "    @allure.description(\"" + testcase["Desc"] + "\")" + "\n"
        testmethod_content = pytest_mark_content + allure_desc_content + testmethod_content
        testmethod_content = testmethod_content.replace('{TESTMETHOD}', testcase[params_type+"ID"])
        # testmethod_content = testmethod_content.replace('{CASEFILENAME}', xmlfile)
        testmethod_content = testmethod_content.replace('{CASEID}', testcase[params_type+"ID"])
        testmethod_content = testmethod_content.replace('{CLEANVALUE}', str(clean_value))
        testmethod_template.close()
        return testmethod_content

    def create_testclass_content(cls,rootdir, classname, projectname, casefilename, classcontent, py_filename):
        testclass_template = open(cls.conf.get('STATIC_VARIABLE','TEST_CLASS_PATH'), mode='r', encoding="utf-8")
        testclass_content = testclass_template.read()
        testclass_content = testclass_content.replace('{ROOTDIR}', rootdir)
        testclass_content = testclass_content.replace('{CLASSNAME}', classname)
        testclass_content = testclass_content.replace('{PROJECTNAME}', projectname)
        testclass_content = testclass_content.replace('{CASEFILENAME}', casefilename)
        testclass_content = testclass_content.replace('{TESTMETHODS}', classcontent)
        testclass_content = testclass_content.replace('{PYFILENAME}', py_filename)
        testclass_template.close()
        return testclass_content

    def create_runpy_content(cls,rootdir, xml_report_dir):
        runpy_template = open(cls.conf.get('STATIC_VARIABLE','RUN_TEMPLATE_PATH'), mode='r', encoding="utf-8")
        runpy_content = runpy_template.read()
        runpy_content = runpy_content.replace('{ROOTDIR}', rootdir)
        runpy_content = runpy_content.replace('{XMLREPORTDIR}', xml_report_dir)
        runpy_template.close()
        return runpy_content

    def create_loggerconf(cls):
        loggerconf_template = open(cls.conf.get('STATIC_VARIABLE','LOGGER_CONFIG_TEMPLATE_PATH'), mode='r', encoding="utf-8")
        loggerconf_content = loggerconf_template.read()
        loggerconf_content = loggerconf_content.replace('{log_folder}', cls.conf.get('STATIC_VARIABLE','LOG_PATH'))
        loggerconf_content = loggerconf_content.replace('{slash}', dir_slash)
        loggerconf_template.close()
        loogerconf_file = open(cls.conf.get('STATIC_VARIABLE','LOG_PATH'), mode='w', encoding="utf-8")
        loogerconf_file.write(loggerconf_content)
        loogerconf_file.close()

    def generate_stepgroups(cls,project_path):
        stepgroup_path = project_path + dir_slash + 'stepgroups'
        datafiles_path = project_path + dir_slash + 'datafiles'
        datafiles_list = os.listdir(datafiles_path)
        print(datafiles_list)
        case_list = cls.fuzzyfinder("case.", datafiles_list)
        for datafile in case_list:
            if datafile.endswith("cases.xml"):
                testcaselist = XmlParseHelp(datafiles_path + dir_slash + datafile).get_testcaselistdict4xml()
            else:
                testcaselist = YamlHelp(datafiles_path + dir_slash + datafile).get_testcaselistdict4yaml()
            stepgroup_content = cls.create_stepgroups_content(testcaselist, project_path)
            stepfile_path = stepgroup_path + dir_slash + testcaselist["StepModule"] + '.py'
            stepfile_name = os.path.split(stepfile_path)[1]
            if os.path.exists(stepfile_path):
                print('{}文件已存在，跳过生成步骤'.format(stepfile_name))
                pass
            else:
                py_filename = cls.set_py_filename(testcaselist) + '.py'
                stepgroupfile = open(stepgroup_path + dir_slash + py_filename, mode="w",
                                     encoding="utf-8")
                stepgroupfile.write(stepgroup_content)
                stepgroupfile.close()

    def generate_config(cls,project_path):
        config_path = project_path + dir_slash + 'config.py'
        if os.path.exists(config_path):
            print('config.py文件已存在，跳过生成步骤')
            pass
        else:
            py_name = 'config.py'
            a = cls.create_config_content()
            configfile = open(project_path + dir_slash + py_name, mode="w", encoding='utf-8')
            configfile.write(a)
            configfile.close()

if __name__ == '__main__':
    Casecreator().create_loggerconf()
    print("*" * 50)
    Casecreator().create_global_runpy()
    projectpath_list = Casecreator().get_projectpath_list()
    print("projectspaths: {}".format(projectpath_list))
    for project_path in projectpath_list:
        Casecreator().create_testproject(project_path)
        Casecreator().generate_testcase(project_path)
        Casecreator().generate_stepgroups(project_path)
        Casecreator().generate_config(project_path)
    # testcase={'Name': '这是name3', 'ID': None, 'CaseTag': None, 'TestSteps': {'Step': {'StepName': None, 'StepParameterID': None}}, 'StepParametersFileName': 'crm_course_detailparameters.xml', 'StepPackage': 'projects.middle_platform.crm.stepgroups', 'StepModule': 'crm_course_detail', 'StepGroup': 'Coursedetail'}
    #
    # Casecreator().create_testmethod_content(testcase)