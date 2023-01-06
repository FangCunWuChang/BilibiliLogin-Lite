from application.module.decoration import application_error

from application.utils import urlQuerySplit

from selenium.webdriver.chrome.service import Service
from urllib.parse import urlsplit
from selenium import webdriver
import base64
import json
import time
import os


class GeeTestContent(object):
    def __init__(self, gee_response_json: dict):
        """ 代替原有gee_values """
        self.gee_challenge = gee_response_json["gee_challenge"]
        self.gee_seccode = gee_response_json["geetest_seccode"]
        self.gee_validate = gee_response_json["geetest_validate"]
        self.recaptcha_token = gee_response_json["recaptcha_token"]

    @property
    def content(self):
        return self.__dict__


class GeeTest(object):
    @application_error
    def __init__(self, gt: str, challenge: str):
        """ 还得是selenium """
        super(GeeTest, self).__init__()

        service = Service(os.path.abspath("geetest/chromedriver.exe"))
        self.driver = webdriver.Chrome(service=service)
        gee_html = os.path.abspath("./geetest/template/index.html")
        self.driver.get(gee_html + f"?gt={gt}&challenge={challenge}")

    @application_error
    def waitFinishing(self, time_sleep: int | float = 1) -> dict:
        """ 获取到极验证数据 """
        _, name = os.path.split(urlsplit(self.driver.current_url).path)
        while name != "finish.html":
            _, name = os.path.split(urlsplit(self.driver.current_url).path)
            time.sleep(time_sleep)
        query_dict = urlQuerySplit(self.driver.current_url)
        self.driver.quit()
        debase64 = base64.b64decode(query_dict["data"]).decode()
        return json.loads(debase64)
