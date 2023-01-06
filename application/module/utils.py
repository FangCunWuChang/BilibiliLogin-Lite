from application.errors import (
    GuiDeviceValueNotExist,
    DidNotEnter,
    TelNumberFormatError,
    CidFormatError,
    VerifyCodeFormatError
)
from application.items import TkinterButton
from application.config import ButtonConfig


class ButtonCommand(object):
    """ 按钮绑定事件 """
    def __init__(self, root, config: ButtonConfig, **kwargs):
        super(ButtonCommand, self).__init__()

        self.root = root
        TkinterButton(self.root, config, func=self.func)

    def func(self):
        """ 事件 """
        ...


def extractCookie(response_json: dict, buvid) -> tuple[str, str]:
    """ 提取 accessKey 和 cookie """
    access_key = str(response_json["data"]["token_info"]["access_token"])
    cookie_list = response_json["data"]["cookie_info"]["cookies"]
    cookie_dict = {li["name"]: li["value"] for li in cookie_list}
    cookie_dict.update({"Buvid": str(buvid)})
    cookie_list = [f"{k}={v}" for k, v in cookie_dict.items()]
    return access_key, "; ".join(cookie_list)


def get_all_device_value(root, error: bool = True) -> dict:
    """ 获取设备信息 """
    device_values = dict({
        "BilibiliBuvid": root["Device_BilibiliBuvid"],
        "AndroidModel": root["Device_AndroidModel"],
        "AndroidBuild": root["Device_AndroidBuild"],
        "VersionName": root["Device_VersionName"],
        "VersionCode": root["Device_VersionCode"]
    })
    if not all(device_values.values()) and error:
        raise GuiDeviceValueNotExist("设备信息未填写/全")
    return device_values


def get_tel_number(root) -> str:
    """ 获取手机号 """
    tel_number = root["tel_entry"].value()
    tel_number = tel_number.replace(" ", "")
    if not tel_number:
        raise DidNotEnter("未输入手机号")
    if not tel_number.isdigit():
        raise TelNumberFormatError("手机号不能带有字符串")
    if len(tel_number) >= 12:
        raise TelNumberFormatError("手机号长度错误")
    return str(tel_number)


def get_cid_number(root) -> str:
    """ 获取地区号 """
    cid_number = root["cid_entry"].value()
    cid_number = cid_number.replace(" ", "")
    if not cid_number:
        raise DidNotEnter("未输入地区号")
    if not cid_number.isdigit():
        raise CidFormatError("地区号不能带有字符串")
    if len(cid_number) >= 5:
        raise CidFormatError("地区号长度错误")
    return str(cid_number)


def get_verify_code(root) -> str:
    """ 获取验证码 """
    verify_code = root["code_entry"].value()
    verify_code = verify_code.replace(" ", "")
    if not verify_code:
        raise DidNotEnter("未输入验证码")
    if not verify_code.isdigit():
        raise VerifyCodeFormatError("验证码不能带有字符串")
    if len(verify_code) != 6:
        raise VerifyCodeFormatError("验证码长度错误")
    return str(verify_code)
