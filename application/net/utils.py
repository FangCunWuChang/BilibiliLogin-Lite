import os
import zipfile

from application.net.session import Session
from application.config import (
    default_net_config, chromedriver_index_url,
    chromedriver_download_url
)


def get_versions(mod: str = "android") -> tuple[str, str]:
    """ 获取[版本号]和[版本名] """
    url = f"https://app.bilibili.com/x/v2/version"
    with Session(**default_net_config) as session:
        res = session.request("GET", url, params={"mobi_app": mod})
    code = str(res.json()["data"][0]["build"])
    name = str(res.json()["data"][0]["version"])
    return code, name


def download_chromedriver(version: str):
    """ 下载对应版本chromedriver """

    url = chromedriver_download_url.format(VERSION=version)

    with Session(**default_net_config) as session:
        res = session.request("GET", url)
    content_length = res.headers.get("content-length")
    now_content_length = 0
    with open("geetest/chromedriver.zip", "wb") as f:
        for content in res.iter_bytes(4096):
            f.write(content)
            now_content_length += len(content)
            print(f"正在下载:{now_content_length}/{content_length}")
    f.close()

    file = zipfile.ZipFile(os.path.abspath("geetest/chromedriver.zip"))
    print('开始解压文件')

    file.extractall(os.path.abspath("geetest/"))
    file.close()

    print("自动更新完成")

    return os.path.abspath("geetest/chromedriver.exe")


def get_chromedriver_list():
    """ 获取版本列表 """
    with Session(**default_net_config) as session:
        res = session.request("GET", chromedriver_index_url)
    chromedriver_names = [i["name"] for i in res.json()]

    chromedriver_list = list()
    for name in chromedriver_names:
        if name[-1] == "/":
            name = name.replace("/", "")
        chromedriver_list.append(name)

    return_list = list()
    for i in chromedriver_list:
        version_list = i.split(".")
        if all([ii.isdigit() for ii in version_list]):
            return_list.append(i)

    return return_list
