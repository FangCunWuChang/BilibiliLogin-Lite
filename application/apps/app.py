from application.errors import GuiValueError

from application.net.utils import get_versions
from application.utils import reader

from application.config import main_button_settings

from application.module.controls import TkinterButton

from application.module.command.main import (
    setting_device, sms_login, password_login
)

from functools import partial
import tkinter
import os


main_func_list = [
    ("sms_login", sms_login),
    ("password_login", password_login),
    ("setting_device", setting_device)
]


class AppDeviceInfo(object):
    def __init__(self):
        """ 设备信息 """
        super(AppDeviceInfo, self).__init__()
        self.Device_Buvid = ""
        self.Device_AndroidModel = ""
        self.Device_AndroidBuild = ""

        code, name = get_versions()

        self.Device_VersionName = str(name)
        self.Device_VersionCode = str(code)

        if os.path.exists("./device.json"):
            device = reader("./device.json")
            self.Device_Buvid = device.get("Buvid", "")
            self.Device_AndroidModel = device.get("AndroidModel", "")
            self.Device_AndroidBuild = device.get("AndroidBuild", "")
            self.Device_VersionName = device.get("VersionName", "")
            self.Device_VersionCode = device.get("VersionCode", "")


class App(tkinter.Tk, AppDeviceInfo):
    def __init__(self):
        super(App, self).__init__()
        AppDeviceInfo.__init__(self)

        self.title("登陆")
        self.configure(background="#f0f0f0")
        self.resizable(False, False)
        self.geometry("200x130")

        for name, func in main_func_list:
            config = main_button_settings[name]
            TkinterButton(self, config, partial(func, self))

    def __setitem__(self, key: str, value) -> any:
        """ 设置 """
        return setattr(self, str(key), value)

    def __getitem__(self, item: str):
        """ 取得 """
        value = getattr(self, str(item), None)
        if value is None:
            raise GuiValueError(f"不存在{item}")
        return value
