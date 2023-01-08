from application.module.utils import (
    ButtonCommand,
    extractCookie,
    get_tel_number,
    get_cid_number,
    get_verify_code,
)
from application.module.decoration import (
    application_error,
    application_thread
)
from application.message import (
    showinfo,
    showwarning,
    asksaveasfile
)
from application.utils import (
    parse_cookies,
    writer,
    urlQuerySplit
)
from application.errors import (
    ResponseError,
    DidNotEnter
)
from application.net.login import (
    SmsLogin,
    PasswordLogin
)
from geetest.geetest import (
    GeeTest,
    GeeTestContent
)
from application.apps.utils import InputWindow


class SmsLoginCommandSendVerifyCode(ButtonCommand):
    """ 短信登陆---发送验证码 """
    def __init__(self, *args, **kwargs):
        super(SmsLoginCommandSendVerifyCode, self).__init__(*args, **kwargs)

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        tel_number = get_tel_number(root=self.root)
        cid_number = get_cid_number(root=self.root)

        versions = (self.root.device.get("VersionName", ""), self.root.device.get("VersionCode", ""))
        systems = (self.root.device.get("AndroidModel", ""), self.root.device.get("AndroidBuild", ""))
        bilibili_login = SmsLogin(versions, systems, self.root.device.get("BilibiliBuvid", ""))

        sms_send_response = bilibili_login.sms_send(cid_number, tel_number, {})

        if sms_send_response.json()["code"] != 0:
            message = sms_send_response.json()["message"]
            raise ResponseError(message or "?")

        self.root.captcha_key = sms_send_response.json()["data"]["captcha_key"]
        if not self.root.captcha_key:
            # 无"captcha_key"需完成人机验证
            recaptcha_url = sms_send_response.json()["data"]["recaptcha_url"]
            query_dict = urlQuerySplit(recaptcha_url)

            showinfo("提示", "完成人机验证以继续")

            gee = GeeTest(query_dict["gee_gt"], query_dict["gee_challenge"])
            gee_verify: dict = gee.waitFinishing(time_sleep=1)
            gee_verify.update({"recaptcha_token": query_dict["recaptcha_token"]})

            gee_content = GeeTestContent(gee_verify)
            tel_and_cid_gee = (cid_number, tel_number, gee_content)
            sms_send_response = bilibili_login.sms_send(*tel_and_cid_gee)

            if sms_send_response.json()["code"] != 0:
                message = sms_send_response.json()["message"]
                raise ResponseError(message or "?")

            self.root.captcha_key = sms_send_response.json()["data"]["captcha_key"]

        if not self.root.captcha_key:
            showwarning("警告", "验证码发送失败")
        else:
            showinfo("提示", "验证码发送成功")


class SmsLoginCommandLoginSms(ButtonCommand):
    def __init__(self, *args, **kwargs):
        super(SmsLoginCommandLoginSms, self).__init__(*args, **kwargs)

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        tel_number = get_tel_number(root=self.root)
        cid_number = get_cid_number(root=self.root)
        verify_code = get_verify_code(root=self.root)

        tel_and_cid = (cid_number, tel_number)

        versions = (self.root.device.get("VersionName", ""), self.root.device.get("VersionCode", ""))
        systems = (self.root.device.get("AndroidModel", ""), self.root.device.get("AndroidBuild", ""))
        bilibili_login = SmsLogin(versions, systems, self.root.device.get("BilibiliBuvid", ""))

        captcha_code = (self.root.captcha_key or "", verify_code)
        login_response = bilibili_login.login_sms(*tel_and_cid, *captcha_code)

        if login_response.json()["code"] != 0:
            message = login_response.json()["message"]
            raise ResponseError(message or "?")

        bilibili_buvid = self.root.device.get("BilibiliBuvid", "")
        access_key, cookie = extractCookie(login_response.json(), bilibili_buvid)

        mid = parse_cookies(cookie)["DedeUserID"]
        save_path = asksaveasfile("保存登陆数据", [("json", "*.json")], f"{mid}.json")
        writer(save_path, {"accessKey": access_key, "cookie": cookie})

        showinfo("提示", "操作完成")


class PasswordLoginCommandOauth2(ButtonCommand):
    def __init__(self, *args, **kwargs):
        super(PasswordLoginCommandOauth2, self).__init__(*args, **kwargs)

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        username = self.root["username_entry"].value()
        password = self.root["password_entry"].value()

        if not username:
            raise DidNotEnter("用户名未输入")
        if not password:
            raise DidNotEnter("密码未输入")

        versions = (self.root.device.get("VersionName", ""), self.root.device.get("VersionCode", ""))
        systems = (self.root.device.get("AndroidModel", ""), self.root.device.get("AndroidBuild", ""))
        bilibili_login = PasswordLogin(versions, systems, self.root.device.get("BilibiliBuvid", ""))

        web_key_response = bilibili_login.web_key()
        if web_key_response.json()["code"] != 0:
            message = web_key_response.json()["message"]
            raise ResponseError(message or "?")

        rsa_key = web_key_response.json()["data"]["key"]
        rsa_hash = web_key_response.json()["data"]["hash"]

        login_args = (username, password, rsa_key, rsa_hash)
        oauth2_response = bilibili_login.oauth2_login(*login_args)

        if oauth2_response.json()["code"] != 0:
            message = oauth2_response.json()["message"]
            raise ResponseError(message or "?")

        if oauth2_response.json()["data"]["status"] != 0:
            showinfo("提示", oauth2_response.json()["data"]["message"] or "?")
            verify_url = oauth2_response.json()["data"]["url"]
            verify_query = urlQuerySplit(verify_url)

            tmp_code = verify_query["tmp_token"]
            verify_query.update({"tmp_code": tmp_code})
            verify_query.pop("tmp_token", None)

            tmp_code = verify_query["tmp_code"]

            info_response = bilibili_login.user_info(tmp_code)
            if info_response.json()["code"] != 0:
                message = info_response.json()["message"]
                raise ResponseError(message or "?")

            captcha_response = bilibili_login.captcha_pre()
            if captcha_response.json()["code"] != 0:
                message = captcha_response.json()["message"]
                raise ResponseError(message or "?")

            gee_dict: dict = captcha_response.json()["data"]
            gee_dict.pop("recaptcha_type", None)

            showinfo("提示", "完成人机验证以继续")

            gee = GeeTest(gee_dict["gee_gt"], gee_dict["gee_challenge"])
            gee_dict.update(gee.waitFinishing(1))

            gee_content = GeeTestContent(gee_dict)

            sms_send_response = bilibili_login.sms_send(tmp_code, gee_content)

            captcha_key = sms_send_response.json()["data"]["captcha_key"]
            tel_text = info_response.json()["data"]["account_info"]["hide_tel"]
            showinfo("提示", f"验证码已发送到[{tel_text}]")

            code = None
            while not code:
                input_app = InputWindow()
                input_app.mainloop()
                args = (tmp_code, captcha_key, input_app.verify_code)
                if "request_id" in verify_query:
                    req = {"request_id": verify_query["request_id"]}
                    login_response = bilibili_login.tel_verify(*args, **req)
                else:
                    login_response = bilibili_login.tel_verify(*args)

                if login_response.json()["code"] != 0:
                    showinfo("提示", login_response.json()["message"] or "?")
                    continue

                code = login_response.json()["data"]["code"]

            oauth2_response = bilibili_login.oauth2_access_token(code)
            if oauth2_response.json()["code"] != 0:
                message = oauth2_response.json()["message"]
                raise ResponseError(message or "?")

        bilibili_buvid = self.root.device.get("BilibiliBuvid", "")
        access_key, cookie = extractCookie(oauth2_response.json(), bilibili_buvid)

        mid = parse_cookies(cookie)["DedeUserID"]
        save_path = asksaveasfile("保存登陆数据", [("json", "*.json")], f"{mid}.json")
        writer(save_path, {"accessKey": access_key, "cookie": cookie})

        showinfo("提示", "操作完成")
