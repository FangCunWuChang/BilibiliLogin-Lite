from application.net.utils import (
    download_chromedriver,
    get_chromedriver_list
)

from selenium.webdriver.chrome.service import Service
from selenium import webdriver

import webbrowser
import sys
import os
import re


def test_open_chromedriver():
    try:
        service = Service(os.path.abspath("geetest/chromedriver.exe"))
        driver = webdriver.Chrome(service=service)
    except Exception as msg:
        ver = re.search(r'browser version is (.+) with', str(msg))
        version = ver.group(1)
        return version or None
    else:
        driver.quit()
        return True


def examine_chromedriver():
    print("正在检查chrome/chromedriver更新")

    version = test_open_chromedriver()
    if version is True:
        print("无需更新")
        return

    chromedriver_list = get_chromedriver_list()

    if version is None:
        webbrowser.open("https://www.google.cn/chrome/")
        sys.exit("未下载chrome，打开https://www.google.cn/chrome/下载已继续")
    version_tuple = version.split(".")

    end_number = int(version_tuple[-1])
    ver = ".".join(version_tuple[0:len(version_tuple) - 1])

    if version not in chromedriver_list:
        list_ = list()
        for li in chromedriver_list:
            if ver in li:
                list_.append(li)
        chromedriver_list = list_

    else:
        return download_chromedriver(version)

    end_number_list = list()
    for i in chromedriver_list:
        end_number_list.append(int(i.split(".")[-1]))
    end_number_list.sort()

    _end_number = None
    for end_number2 in end_number_list:
        if end_number2 >= end_number:
            _end_number = end_number2
            break

    if _end_number is None:
        _end_number = end_number_list[-1]

    return download_chromedriver(f"{ver}.{_end_number}")


if __name__ == '__main__':
    if sys.argv[-1] != "-disable":
        examine_chromedriver()

    from application.apps.app import App
    app = App()
    app.mainloop()
