from urllib.parse import urlencode

from application.net.session import Session

from application.utils import (
    LOGIN_SIGN, rsaPassword, build_x_bili_trace_id, FormData
)

from application.module.decoration import application_error

from application.config import login_config

import time


class SmsLogin(object):
    @application_error
    def __init__(self, versions: tuple[str, str], system: tuple[str, str], buvid: str):
        super(SmsLogin, self).__init__()

        (self.name, self.code), (self.model, self.os_ver) = versions, system
        statistics = '{"appId":1,"platform":3,"version":"%s","abtest":""}'
        self.statistics, self.buvid = statistics % (self.name,), buvid

    @application_error
    def sms_send(self, cid: str, tel: str, **kwargs):
        headers: dict = login_config["sms_send"]["headers"]
        headers.update({"Buvid": str(self.buvid)})
        user_agent = headers["User-Agent"].format(
            MODEL=self.model, OSVER=self.os_ver,
            NAME=self.name, CODE=self.code
        )
        headers.update({"User-Agent": user_agent})

        url = "https://passport.bilibili.com/x/passport-login/sms/send"

        ts = round(time.time())

        form_data = FormData({
            "build": self.code,
            "buvid": self.buvid,
            "channel": "alifenfa",
            "cid": cid,
            "disable_rcmd": "0",
            "local_id": self.buvid,
            "mobi_app": "android",
            "platform": "android",
            "statistics": self.statistics,
            "tel": tel,
            "ts": ts,
            **kwargs
        }).toSign(LOGIN_SIGN)

        data = urlencode(form_data)

        headers.update({"Content-Length": str(len(data))})
        _trace_id = build_x_bili_trace_id(ts)
        headers.update({"x-bili-trace-id": _trace_id})

        with Session(headers=headers) as client:
            res = client.request("POST", url, data=data)
        return res

    @application_error
    def login_sms(self, cid: str, tel: str, captcha: str, code: str):
        headers: dict = login_config["login_sms"]["headers"]
        headers.update({"Buvid": str(self.buvid)})
        user_agent = headers["User-Agent"].format(
            MODEL=self.model, OSVER=self.os_ver,
            NAME=self.name, CODE=self.code
        )
        headers.update({"User-Agent": user_agent})

        url = "https://passport.bilibili.com/x/passport-login/login/sms"

        ts = round(time.time())

        form_data = FormData({
            "build": self.code,
            "buvid": self.buvid,
            "captcha_key": captcha,
            "channel": "alifenfa",
            "cid": cid,
            "code": code,
            "disable_rcmd": "0",
            "local_id": self.buvid,
            "mobi_app": "android",
            "platform": "android",
            "statistics": self.statistics,
            "tel": tel,
            "ts": ts
        }).toSign(LOGIN_SIGN)

        data = urlencode(form_data)

        headers.update({"Content-Length": str(len(data))})
        _trace_id = build_x_bili_trace_id(ts)
        headers.update({"x-bili-trace-id": _trace_id})

        with Session(headers=headers) as client:
            res = client.request("POST", url, data=data)
        return res


class PasswordLogin(object):
    @application_error
    def __init__(self, versions: tuple[str, str], system: tuple[str, str], buvid: str):
        super(PasswordLogin, self).__init__()

        (self.name, self.code), (self.model, self.os_ver) = versions, system
        statistics = '{"appId":1,"platform":3,"version":"%s","abtest":""}'
        self.statistics, self.buvid = statistics % (self.name,), buvid

    @application_error
    def web_key(self):
        """ 获取登陆所需的key """
        headers: dict = login_config["web_key"]["headers"]
        headers.update({"Buvid": str(self.buvid)})
        user_agent = headers["User-Agent"].format(
            MODEL=self.model, OSVER=self.os_ver,
            NAME=self.name, CODE=self.code
        )
        headers.update({"User-Agent": user_agent})

        url = "https://passport.bilibili.com/x/passport-login/web/key"

        ts = round(time.time())

        params_data = FormData({
            "build": self.code,
            "buvid": self.buvid,
            "channel": "alifenfa",
            "disable_rcmd": "0",
            "local_id": self.buvid,
            "mobi_app": "android",
            "platform": "android",
            "statistics": self.statistics,
            "ts": ts
        }).toSign(LOGIN_SIGN)

        params = urlencode(params_data)

        _trace_id = build_x_bili_trace_id(ts)
        headers.update({"x-bili-trace-id": _trace_id})

        with Session(headers=headers) as client:
            res = client.request("GET", url, params=params)
        return res

    @application_error
    def oauth2_login(self, username: str, password: str, key: str, rhash: str):
        """ 登陆 """
        headers: dict = login_config["oauth2_login"]["headers"]
        headers.update({"Buvid": str(self.buvid)})
        user_agent = headers["User-Agent"].format(
            MODEL=self.model, OSVER=self.os_ver,
            NAME=self.name, CODE=self.code
        )
        headers.update({"User-Agent": user_agent})

        url = "https://passport.bilibili.com/x/passport-login/oauth2/login"

        ts = round(time.time())

        form_data = FormData({
            "build": self.code,
            "buvid": self.buvid,
            "channel": "alifenfa",
            "disable_rcmd": "0",
            "local_id": self.buvid,
            "mobi_app": "android",
            "password": rsaPassword(password, key, rhash),
            "platform": "android",
            "s_locale": "zh_CN",
            "statistics": self.statistics,
            "ts": ts,
            "username": username
        }).toSign(LOGIN_SIGN)

        data = urlencode(form_data)

        headers.update({"Content-Length": str(len(data))})
        _trace_id = build_x_bili_trace_id(ts)
        headers.update({"x-bili-trace-id": _trace_id})

        with Session(headers=headers) as client:
            res = client.request("POST", url, data=data)
        return res

    @application_error
    def captcha_pre(self):
        headers: dict = login_config["captcha_pre"]["headers"]
        user_agent = headers["User-Agent"].format(
            MODEL=self.model, OSVER=self.os_ver,
            NAME=self.name, CODE=self.code
        )
        headers.update({"User-Agent": user_agent})

        url = "https://passport.bilibili.com/x/safecenter/captcha/pre"

        ts = round(time.time())

        form_data = FormData({
            "disable_rcmd": "0",
            "statistics": self.statistics,
            "ts": ts
        }).toSign(LOGIN_SIGN)

        data = urlencode(form_data)

        headers.update({"Content-Length": str(len(data))})
        _trace_id = build_x_bili_trace_id(ts)
        headers.update({"x-bili-trace-id": _trace_id})

        _cookie = {"Buvid": self.buvid}
        with Session(headers=headers, cookies=_cookie) as client:
            res = client.request("POST", url, data=data)
        return res

    @application_error
    def sms_send(self, tmp_code: str, **kwargs):
        headers: dict = login_config["password_sms_send"]["headers"]
        user_agent = headers["User-Agent"].format(
            MODEL=self.model, OSVER=self.os_ver,
            NAME=self.name, CODE=self.code
        )
        headers.update({"User-Agent": user_agent})

        url = "https://passport.bilibili.com/x/safecenter/common/sms/send"

        ts = round(time.time())

        form_data = FormData({
            "disable_rcmd": "0",
            "sms_type": "loginTelCheck",
            "statistics": self.statistics,
            "tmp_code": tmp_code,
            "ts": ts,
            **kwargs
        }).toSign(LOGIN_SIGN)

        data = urlencode(form_data)

        headers.update({"Content-Length": str(len(data))})
        _trace_id = build_x_bili_trace_id(ts)
        headers.update({"x-bili-trace-id": _trace_id})

        _cookie = {"Buvid": self.buvid}
        with Session(headers=headers, cookies=_cookie) as client:
            res = client.request("POST", url, data=data)
        return res

    @application_error
    def user_info(self, tmp_code: str):
        headers: dict = login_config["user_info"]["headers"]
        user_agent = headers["User-Agent"].format(
            MODEL=self.model, OSVER=self.os_ver,
            NAME=self.name, CODE=self.code
        )
        headers.update({"User-Agent": user_agent})

        url = "https://passport.bilibili.com/x/safecenter/user/info"

        ts = round(time.time())

        params_data = FormData({
            "disable_rcmd": "0",
            "statistics": self.statistics,
            "tmp_code": tmp_code,
            "ts": ts
        }).toSign(LOGIN_SIGN)

        params = urlencode(params_data)

        _trace_id = build_x_bili_trace_id(ts)
        headers.update({"x-bili-trace-id": _trace_id})

        _cookie = {"Buvid": self.buvid}
        with Session(headers=headers, cookies=_cookie) as client:
            res = client.request("GET", url, params=params)
        return res

    @application_error
    def tel_verify(self, tmp_code: str, captcha_key: str, code: str | int, **kwargs):
        headers: dict = login_config["password_sms_send"]["headers"]
        user_agent = headers["User-Agent"].format(
            MODEL=self.model, OSVER=self.os_ver,
            NAME=self.name, CODE=self.code
        )
        headers.update({"User-Agent": user_agent})

        url = "https://passport.bilibili.com/x/safecenter/login/tel/verify"

        ts = round(time.time())

        form_data = FormData({
            "build": self.code,
            "buvid": self.buvid,
            "captcha_key": captcha_key,
            "code": code,
            "disable_rcmd": "0",
            "local_id": self.buvid,
            "source": "risk",
            "statistics": self.statistics,
            "tmp_code": tmp_code,
            "ts": ts,
            "type": "loginTelCheck",
            **kwargs
        }).toSign(LOGIN_SIGN)

        data = urlencode(form_data)

        headers.update({"Content-Length": str(len(data))})
        _trace_id = build_x_bili_trace_id(ts)
        headers.update({"x-bili-trace-id": _trace_id})

        _cookie = {"Buvid": self.buvid}
        with Session(headers=headers, cookies=_cookie) as client:
            res = client.request("POST", url, data=data)
        return res

    @application_error
    def oauth2_access_token(self, code: str):
        headers: dict = login_config["password_sms_send"]["headers"]
        headers.update({"Buvid": str(self.buvid)})
        user_agent = headers["User-Agent"].format(
            MODEL=self.model, OSVER=self.os_ver,
            NAME=self.name, CODE=self.code
        )
        headers.update({"User-Agent": user_agent})

        url = "https://passport.bilibili.com/x/passport-login/oauth2/access_token"

        ts = round(time.time())

        form_data = FormData({
            "build": self.code,
            "buvid": self.buvid,
            "channel": "alifenfa",
            "code": code,
            "disable_rcmd": "0",
            "grant_type": "authorization_code",
            "local_id": self.buvid,
            "mobi_app": "android",
            "platform": "android",
            "statistics": self.statistics,
            "ts": ts
        }).toSign(LOGIN_SIGN)

        data = urlencode(form_data)

        headers.update({"Content-Length": str(len(data))})
        _trace_id = build_x_bili_trace_id(ts)
        headers.update({"x-bili-trace-id": _trace_id})

        with Session(headers=headers) as client:
            res = client.request("POST", url, data=data)
        return res
