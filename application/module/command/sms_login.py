from application.module.decoration import (
    application_thread, application_error
)

from application.errors import (
    FormatError, ResponseError
)

from application.utils import (
    urlQuerySplit, extractCookie,
    parse_cookies, writer
)

from application.message import (
    showinfo, showwarning, asksaveasfile
)

from geetest.geetest import GeeTest


@application_thread
@application_error
def sms_send_verify_code(master, _) -> None:
    tel_number = master["tel_number_entry"].value("未输入手机号")
    tel_number = tel_number.replace(" ", "")
    if not tel_number.isdigit():
        raise FormatError("手机号格式不正确")

    cid_number = master["cid_entry"].value("未输入区号")
    cid_number = cid_number.replace(" ", "")
    if not cid_number.isdigit():
        raise FormatError("区号格式不正确")

    tel_and_cid = (cid_number, tel_number)

    sms_send_res = master.login.sms_send(*tel_and_cid)

    if sms_send_res.json()["code"] != 0:
        message = sms_send_res.json()["message"]
        raise ResponseError(message)

    master.captcha_key = sms_send_res.json()["data"]["captcha_key"]

    if not master.captcha_key:
        recaptcha_url = sms_send_res.json()["data"]["recaptcha_url"]
        query_dict = urlQuerySplit(recaptcha_url)

        showinfo("提示", "完成人机验证以继续")

        gee = GeeTest(query_dict["gee_gt"], query_dict["gee_challenge"])
        gee_verify = gee.waitFinishing(time_sleep=1)

        gee_form_data = {
            "gee_challenge": gee_verify["geetest_challenge"],
            "gee_seccode": gee_verify["geetest_seccode"],
            "gee_validate": gee_verify["geetest_validate"],
            "recaptcha_token": query_dict["recaptcha_token"],
        }

        sms_send_res = master.login.sms_send(*tel_and_cid, **gee_form_data)

        if sms_send_res.json()["code"] != 0:
            message = sms_send_res.json()["message"]
            raise ResponseError(message)

        master.captcha_key = sms_send_res.json()["data"]["captcha_key"]

    if not master.captcha_key:
        showwarning("提示", "验证码发送失败")
    else:
        showinfo("提示", "验证码发送成功")


@application_thread
@application_error
def sms_login_login(master, buvid):
    if not master.captcha_key:
        showinfo("提示", "未成功发送验证码")
        return

    tel_number = master["tel_number_entry"].value("未输入手机号")
    tel_number = tel_number.replace(" ", "")
    if not tel_number.isdigit():
        raise FormatError("手机号格式不正确")

    cid_number = master["cid_entry"].value("未输入区号")
    cid_number = cid_number.replace(" ", "")
    if not cid_number.isdigit():
        raise FormatError("区号格式不正确")

    tel_and_cid = (cid_number, tel_number)

    verify_code = master["verify_code_entry"].value("未输入验证码")
    verify_code = verify_code.replace(" ", "")
    if not verify_code.isdigit():
        raise FormatError("验证码格式不正确")

    captcha_code = (master.captcha_key, verify_code)

    login_res = master.login.login_sms(*tel_and_cid, *captcha_code)

    if login_res.json()["code"] != 0:
        message = login_res.json()["message"]
        raise ResponseError(message)

    access_key, cookie = extractCookie(login_res.json(), buvid)

    mid = parse_cookies(cookie)["DedeUserID"]
    type_ = [("json", "*.json")]
    save_path = asksaveasfile("保存登陆数据", type_, f"{mid}.json")

    writer(save_path, {"accessKey": access_key, "cookie": cookie})

    showinfo("提示", "操作完成")
