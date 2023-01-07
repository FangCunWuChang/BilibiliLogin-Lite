import hashlib
import requests
from urllib.parse import urlencode

from application.net.session import Session
from application.config import (
    default_net_config,
    chromedriver_index_url,
    chromedriver_download_url
)


class FormData(dict):
    """ 表单 """
    def __init__(self, *args, **kwargs):
        super(FormData, self).__init__(*args, **kwargs)

    @property
    def sorted(self):
        """ 排序 """
        return {k: self[k] for k in sorted(self)}

    def toSign(self, app: tuple[str, str]):
        """ 计算sign """
        appkey, appsec = app
        self.update({"appkey": appkey})
        form_data = self.sorted
        text = urlencode(form_data) + appsec
        hashlib_md5 = hashlib.md5()
        hashlib_md5.update(text.encode())
        sign = hashlib_md5.hexdigest()
        form_data.update({"sign": sign})
        return form_data


def get_versions(mod: str = "android") -> tuple[str, str]:
    """ 获取[版本号]和[版本名] """
    url = f"https://app.bilibili.com/x/v2/version"
    with Session(**default_net_config) as session:
        res = session.request("GET", url, params={"mobi_app": mod})
    code = str(res.json()["data"][0]["build"])
    name = str(res.json()["data"][0]["version"])
    return code, name


def download_chromedriver(version: str) -> tuple[requests.Response, int]:
    """ 下载对应版本chromedriver """

    url = chromedriver_download_url.format(VERSION=version)

    with Session(**default_net_config) as session:
        res = session.request("GET", url, stream=True)
    content_length = res.headers.get("content-length")

    return res, int(content_length)


def get_chromedriver_list() -> list[str]:
    """ 获取版本列表 """
    with Session(**default_net_config) as session:
        res = session.request("GET", chromedriver_index_url)
    chromedriver_names = [i["name"] for i in res.json()]
    chromedriver_list = [i[:-1] for i in chromedriver_names]

    versions = list()
    for i in chromedriver_list:
        version_list = i.split(".")
        if len(version_list) != 4:
            continue
        if all([ii.isdigit() for ii in version_list]):
            versions.append(i)

    versions.sort(key=lambda x: tuple(int(v) for v in x.split(".")))

    return versions
