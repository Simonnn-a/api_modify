'''
该脚本用来批量运行该项目下符号条件的case
命令行调用，可以跟持续集成结合，生成的xml报告再跟allure（jenkins有插件）结合展示可视化报告
如命令行运行 python3 run.py 后面不接任何参数，则会运行该项目下testcases目录里的所有case
也支持在后面增加 --casetag param，用来运行指定标签的case
    举例：python3 run.py --casetag BVT+P0,P1  表示运行该项目下有bvt加P0双标签的case或者有P1标签的case
--timeout 5 设置超时限制为5秒   --env dev 设置环境为dev  --monitor 1 开启线上监控模式
'''
import sys
import argparse
FRAME_ROOT_PATH = r'E:\api_modif'
sys.path.append(FRAME_ROOT_PATH)
from settings import GlobalConfig
import pytest
import os,shutil,time

xml_report_dir = r'E:\api_modif\projects\demo\report\xml'
monitor = False

def rm_dir(path):
    if os.path.exists(path):
        if sys.platform == "win32":
            os.system("rmdir /s /q %s" % path)
        else:
            shutil.rmtree(path)

def get_pytest_casetag(args_casetag):
    pytest_casetag = ""
    if args_casetag:
        if "+" in args_casetag:
            args_casetag = args_casetag.replace("+", " and ")  # --casetag 后面的参数里用+号代表组合标记，即同时拥有两个及以上标记的case
        if "," in args_casetag:
            args_casetag = args_casetag.replace(",", " or ")  # --casetag后面的参数里用,号代表多选标签，或者的意思
        if "!" in args_casetag:
            args_casetag = args_casetag.replace("!", "not ")  # --casetag后面的参数里用-号代表反选标签
        pytest_casetag = args_casetag
    else:
        pytest_casetag = "not production"
    return pytest_casetag


def run_test(pytest_casetag):
    GlobalConfig.LASTFAILED = False
    GlobalConfig.FAILEDINFO = None
    rm_dir(xml_report_dir)
    pytest_args=['-s', '-q', '--alluredir', xml_report_dir, '-m']
    # print("-------------------------------pytest_args: ",pytest_args)
    pytest_args.append(pytest_casetag)
    pytest.main(pytest_args)

def run_test_monitor(pytest_casetag):
    serial_fail_times = 0
    while True:
        if GlobalConfig.LASTFAILED == False:
            serial_fail_times = 0
            print("last test success,sleep 30 m")
            time.sleep(30*60)
            run_test(pytest_casetag)
        else:
            serial_fail_times += 1
            rerun_delay = (serial_fail_times + 1) * 60
            if rerun_delay > 600:
                rerun_delay = 600
            GlobalConfig.FAILEDINFO += "连续失败第{}次，将在{}分钟后重跑".format(serial_fail_times, rerun_delay/60)
            print(GlobalConfig.FAILEDINFO)
            if GlobalConfig.ENV == "production":
                from ihuman_common.sendMessage import send_sms_for_project
                send_sms_for_project(GlobalConfig.NOWPROJECT, GlobalConfig.FAILEDINFO)
            print("The test failed {} times in a row,will be rerun in {} s".format(serial_fail_times, rerun_delay))
            time.sleep(rerun_delay)
            run_test(pytest_casetag)

def parse_args():
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--casetag', type=str, default=None)  # 添加--casetag 这个命令行参数，用来运行指定标记的case
    parser.add_argument('--env', type=str, default=None)  # 添加--env 这个命令行参数，用来指定测试环境
    parser.add_argument('--timeout', type=int, default=None)  # 添加--timeout 这个命令行参数，用来指定测试超时时间
    parser.add_argument('--monitor', type=int, default=None)  # 指定是否是监控测试，将循环执行并发报警短信
    args = parser.parse_args()
    if args.env:
        GlobalConfig.ENV = args.env
    if args.timeout:
        GlobalConfig.TIMEOUT = args.timeout
    if args.monitor:
        global monitor
        monitor = True
    args_casetag = args.casetag
    return args_casetag

def main():
    args_casetag = parse_args()
    pytest_casetag = get_pytest_casetag(args_casetag)
    run_test(pytest_casetag)
    if GlobalConfig.TIMEOUTSALLOWED==1:
        time.sleep(120)
        pytest.main(['-s', '-q', GlobalConfig.get_rootdir() + GlobalConfig.get_slash() + GlobalConfig.TIMEOUTITEM])
    if monitor:
        run_test_monitor(pytest_casetag)
    else:
        if GlobalConfig.FAILEDINFO and GlobalConfig.ENV == "production":
            from ihuman_common.sendMessage import send_sms_for_project
            sms_info = GlobalConfig.FAILEDINFO + "Next test will start in 2-10m"
            send_sms_for_project(GlobalConfig.NOWPROJECT, sms_info)



if __name__ == "__main__":
    main()