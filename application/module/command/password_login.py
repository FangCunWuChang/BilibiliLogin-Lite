from application.module.decoration import (
    application_thread, application_error
)

from application.errors import ResponseError

from application.utils import (
    urlQuerySplit, extractCookie,
    parse_cookies, writer
)

from application.message import (
    showinfo, asksaveasfile
)

from geetest.geetest import GeeTest

from application.apps.windows.app import TopWindow

from application.config import (
    password_verify_label_settings,
    password_verify_entry_settings,
    password_verify_button_settings
)

from application.module.controls import (
    TkinterLabel, TkinterButton, TkinterEntry
)

import time


class InputWindow(TopWindow):
    def __init__(self, title, geometry):
        super(InputWindow, self).__init__(title, geometry)

        for label_config in password_verify_label_settings:
            TkinterLabel(self, label_config)

        for name, entry_config in password_verify_entry_settings.items():
            self[f"{name}_entry"] = TkinterEntry(self, entry_config)

        config = password_verify_button_settings["committed"]

        TkinterButton(self, config, self.committed)

        self.code = None

    @application_thread
    @application_error
    def committed(self):
        self.code = self["verify_code_entry"].value(False)

    @application_error
    def results(self):
        while not self.code:
            time.sleep(0.05)
        self.destroy()
        return self.code


@application_thread
@application_error
def password_login_login(master, buvid) -> None:
    username = master["username_entry"].value("未输入账号")
    password = master["password_entry"].value("未输入密码")

    username = username.replace(" ", "")
    password = password.replace(" ", "")

    res_web_key = master.login.web_key()

    if res_web_key.json()["code"] != 0:
        message = res_web_key.json()["message"]
        raise ResponseError(message)

    rsa_key = res_web_key.json()["data"]["key"]
    rsa_hash = res_web_key.json()["data"]["hash"]

    login_args = (username, password, rsa_key, rsa_hash)
    res_login = master.login.oauth2_login(*login_args)

    if res_login.json()["code"] != 0:
        message = res_login.json()["message"]
        raise ResponseError(message)

    if res_login.json()["data"]["status"] != 0:

        showinfo("提示", res_login.json()["data"]["message"] or "?")

        verify_url = res_login.json()["data"]["url"]

        verify_query = urlQuerySplit(verify_url)

        tmp_code = verify_query["tmp_token"]
        verify_query.update({"tmp_code": tmp_code})
        verify_query.pop("tmp_token", None)

        info_res = master.login.user_info(verify_query["tmp_code"])
        if info_res.json()["code"] != 0:
            message = info_res.json()["message"]
            raise ResponseError(message)

        captcha_pre_res = master.login.captcha_pre()
        if captcha_pre_res.json()["code"] != 0:
            message = captcha_pre_res.json()["message"]
            raise ResponseError(message)

        gee_dict: dict = captcha_pre_res.json()["data"]
        gee_dict.pop("recaptcha_type", None)

        showinfo("提示", "完成人机验证以继续")

        gee = GeeTest(gee_dict["gee_gt"], gee_dict["gee_challenge"])
        gee_dict.update(gee.waitFinishing(1))

        gee_data = {
            "gee_challenge": gee_dict["gee_challenge"],
            "gee_seccode": gee_dict["geetest_seccode"],
            "gee_validate": gee_dict["geetest_validate"],
            "recaptcha_token": gee_dict["recaptcha_token"]
        }

        sms_send_res = master.login.sms_send(verify_query["tmp_code"], **gee_data)

        captcha_key = sms_send_res.json()["data"]["captcha_key"]
        tel_text = info_res.json()["data"]["account_info"]["hide_tel"]
        showinfo("提示", f"验证码已发送到[{tel_text}]")

        code = None
        while not code:
            input_win = InputWindow("输入验证码", "300x50")
            verify_code = input_win.results()

            aa = (tmp_code, captcha_key, verify_code)
            if "request_id" in verify_code:
                req = {"request_id": verify_query["request_id"]}
                login_res = master.login.tel_verify(*aa, **req)
            else:
                login_res = master.login.tel_verify(*aa)

            if login_res.json()["code"] != 0:
                showinfo("提示", login_res.json()["message"])
                continue

            code = login_res.json()["data"]["code"]

        res_login = master.login.oauth2_access_token(code)
        if res_login.json()["code"] != 0:
            message = res_login.json()["message"]
            raise ResponseError(message)

    access_key, cookie = extractCookie(res_login.json(), buvid)
    mid = parse_cookies(cookie)["DedeUserID"]
    save_path = asksaveasfile("保存登陆数据", [("json", "*.json")], f"{mid}.json")
    writer(save_path, {"accessKey": access_key, "cookie": cookie})
    showinfo("提示", "操作完成")
