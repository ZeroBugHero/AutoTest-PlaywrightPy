import os
import pytest
import time
from utils import check_browser_installation as cbi
from plugins.read_application import get_application_config
from utils.println import println


def run_cases():
    if cbi.check_browser_installation():
        println('green', "\n浏览器客户端已安装,正在运行用例...\n")
        # 运行指定用例，生成报告放在指定目录
        reports_path = get_application_config().get("reports_path")
        now = time.strftime("%H_%M_%S", time.localtime(time.time()))
        today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        # pytest.main(['-s', '-v', 'cases/login/test_login.py::TestLogin::test_login',
        #              '--alluredir', f'{reports_path.get("allure")}/{today}/{now}'])
        pytest.main(
            ['-s', '-v', 'cases/login/test_login.py::TestLogin',
             '--alluredir', f'{reports_path.get("allure")}/{today}/{now}'])
        # 使用allure生成报告
        println('green', '\n用例运行完成,正在生成报告,请稍后...\n')
        # allure generate report/ -o report/html --clean
        os.system(
            f'allure generate {reports_path.get("allure")}/{today}/{now} -o '
            f'{reports_path.get("html")}/{today}/{now} --clean')
        println('green', '\n用例运行完成,报告生成完成,请查看\n')
        return
    else:
        println('yellow', '\n未安装浏览器客户端,正在安装浏览器客户端,请稍后...\n')
        cbi.install_browser()
        println('green', '\n浏览器客户端安装完成,请重新运行用例\n')


if __name__ == '__main__':
    run_cases()
