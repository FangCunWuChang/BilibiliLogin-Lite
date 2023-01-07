import webbrowser
import sys
import re
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from application.net.utils import (
    get_chromedriver_list, download_chromedriver
)
from application.errors import ChromedriverUpgradeError
from application.config import chromedriver_file


def searchVersions(version: list, chromedriver_list: list):
    """ 搜索可用版本 """
    assert len(version) == 4, ChromedriverUpgradeError("版本非4位")
    version_list, choose = list(), list()
    for i in range(len(version)):
        for li in chromedriver_list:
            if version[i] == li[i]:
                version_list.append(li[i])
                choose.append(li)
        if len(version_list) != i + 1:
            number = [int(i) for i in choose]
            number.sort()
            for nu in number:
                if nu > int(version[i]):
                    version_list.append(version[i])
                    break
        choose = list()
    return ".".join(version_list)


def updateVersions():
    """ 获取最新版本列表 """
    chromedriver_list = get_chromedriver_list()
    chromedriver_list_tuple: list[list] = list()
    for version in chromedriver_list:
        ver = version.split(".")
        if len(ver) == 4:
            chromedriver_list_tuple.append(ver)
    return chromedriver_list_tuple


def init_chromedriver():
    """ 尝试打开chromedriver """
    try:
        service = Service(os.path.abspath(chromedriver_file))
        driver = webdriver.Chrome(service=service)
    except Exception as msg:
        ver = re.search(r'browser version is (.+) with', str(msg))
        if ver is None:
            return None
        version = ver.group(1)
        return version
    else:
        driver.quit()
        return True


def upgradeChromedriver():
    """ 检查chrome/chromedriver更新 """
    print("在检查chrome/chromedriver更新")
    ver = init_chromedriver()
    chromedriver_list = updateVersions()
    if ver is True:
        print("无需更新")
        return
    if ver is None:
        webbrowser.open("https://www.google.cn/chrome/")
        sys.exit("似乎未下载Chrome[https://www.google.cn/chrome/]")
    vers = ver.split(".")
    if len(vers) < 4:
        vers += ["0" for _ in range(4 - len(vers))]
    version = searchVersions(vers, chromedriver_list)
    print(version)
    return download_chromedriver(version)
