import webbrowser
import zipfile
import sys
import re
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from application.net.utils import get_chromedriver_list
from application.apps.utils import ProgressWindow
from application.config import chromedriver_file
from application.message import askyesno


def extract_chromedriver(chromedriver_file_zip: str) -> bool:
    """ 提取chromedriver """
    file = zipfile.ZipFile(chromedriver_file_zip)
    file.extractall(os.path.abspath("geetest/"))
    file.close()
    return os.path.exists(chromedriver_file)


def download_window(version: str) -> str:
    """ 打开下载窗口 """
    root = ProgressWindow(version)
    root.mainloop()
    return root.chromedriver_file_zip


def contrastVersion(current: str, expected: str) -> list[float]:
    """ 比较版本 """
    current, expected = current.split("."), expected.split(".")

    if len(current) <= len(expected):
        current += ["0" for _ in range(len(expected) - len(current))]
    else:
        current = [current[i] for i in range(len(expected))]

    current = [int(i) for i in current]
    expected = [int(i) for i in expected]

    judge_list = list()

    for i in range(len(current)):
        d = int(expected[i] - current[i])
        multiple = 10 ** (len(current) - i)
        judge_list.append(d * multiple / 10)

    return judge_list


def searchVersion(chrome_version: str, versions: list[str]) -> str:
    """ 检查版本 """
    sum_version_content = dict()
    for expected_version in versions:
        judge_list = contrastVersion(chrome_version, expected_version)
        sum_version_content[sum(judge_list)] = expected_version
    chrome_key = min(sum_version_content, key=lambda x: abs(x - 0))
    return sum_version_content[chrome_key]


def init_chromedriver() -> bool | str | None:
    """ 尝试启动chromedriver """
    if not os.path.exists(chromedriver_file):
        return False
    try:
        service = Service(os.path.abspath(chromedriver_file))
        driver = webdriver.Chrome(service=service)
    except Exception as error:
        pattern = r"browser version is (.+) with"
        rsp = re.search(pattern, str(error))
        if rsp is None:
            return None
        return rsp.group(1)
    else:
        driver.quit()
        return True


def upgradeChromedriver() -> None:
    """ 检查chrome/chromedriver更新 """

    print("开始检查chromedriver更新")
    chromedriver_list = get_chromedriver_list()

    # 自检查8次, 过不了直接启动
    for _ in range(8):
        chromedriver_state = init_chromedriver()
        if chromedriver_state is None:
            if askyesno("跳转", "未找到Chrome, 是否前往下载?"):
                webbrowser.open("https://www.google.cn/chrome/")
            sys.exit("未找到Chrome[https://www.google.cn/chrome/]")
        elif chromedriver_state is True:
            print("无需更新")
            break
        elif chromedriver_state is False:
            print("找不到[geetest/chromedriver.exe]")
            zip_file = download_window(chromedriver_list[-1])
            extract_chromedriver(zip_file)
            os.remove(zip_file)
        elif isinstance(chromedriver_state, str):
            print(f"需要更新, Chrome版本[{chromedriver_state}]")
            args = (chromedriver_state, chromedriver_list)
            version = searchVersion(*args)
            zip_file = download_window(version)
            extract_chromedriver(zip_file)
            os.remove(zip_file)

    print("检查chromedriver更新完成")
    return
