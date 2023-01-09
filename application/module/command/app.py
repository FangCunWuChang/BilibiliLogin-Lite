from application.net.utils import get_versions

from application.module.utils import (
    ButtonCommand, get_all_device_value
)
from application.module.decoration import (
    application_error,
    application_thread
)
from application.items import (
    AppConfig,
    ButtonConfig,
    LabelConfig,
    EntryConfig
)
from application.config import (
    font_0, font_1, font_2
)


class AppCommandSmsLogin(ButtonCommand):
    def __init__(self, *args, **kwargs):
        super(AppCommandSmsLogin, self).__init__(*args, **kwargs)

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        from application.apps.windows import SmsLoginWindow
        device = get_all_device_value(self.root)
        app = SmsLoginWindow(AppConfig("短信登陆", "#f0f0f0", False, "300x130"), device)

        app.loadLabel(LabelConfig("手机号", font_2, w=75, h=30, x=10, y=10))
        app.loadLabel(LabelConfig("验证码", font_2, w=75, h=30, x=10, y=50))
        app.loadLabel(LabelConfig("地区号", font_2, w=75, h=30, x=10, y=90))

        app.loadEntry("tel_entry", EntryConfig(None, font_1, w=185, h=30, x=100, y=10))
        app.loadEntry("cid_entry", EntryConfig("86", font_1, w=50, h=30, x=100, y=90))
        app.loadEntry("code_entry", EntryConfig(None, font_1, w=105, h=30, x=100, y=50))

        from application.module.command.login import (
            SmsLoginCommandSendVerifyCode as Func4SendCode,
            SmsLoginCommandLoginSms as Func4LoginSms
        )

        app.loadButton(Func4SendCode, ButtonConfig("发送", font_0, w=65, h=30, x=220, y=50))
        app.loadButton(Func4LoginSms, ButtonConfig("登陆", font_0, w=125, h=30, x=160, y=90))


class AppCommandPasswordLogin(ButtonCommand):
    def __init__(self, *args, **kwargs):
        super(AppCommandPasswordLogin, self).__init__(*args, **kwargs)

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        from application.apps.windows import PasswordLoginWindow
        device = get_all_device_value(self.root)
        app = PasswordLoginWindow(AppConfig("账密登陆", "#f0f0f0", False, "300x130"), device)

        app.loadLabel(LabelConfig("账号", font_2, w=50, h=30, x=10, y=10))
        app.loadLabel(LabelConfig("密码", font_2, w=50, h=30, x=10, y=50))

        app.loadEntry("password_entry", EntryConfig(None, font_1, w=210, h=30, x=75, y=50))
        app.loadEntry("username_entry", EntryConfig(None, font_1, w=210, h=30, x=75, y=10))

        from application.module.command.login import PasswordLoginCommandOauth2 as Func4Oauth2
        app.loadButton(Func4Oauth2, ButtonConfig("登陆", font_0, w=280, h=30, x=10, y=90))


class AppCommandDeviceSetting(ButtonCommand):
    def __init__(self, *args, **kwargs):
        super(AppCommandDeviceSetting, self).__init__(*args, **kwargs)

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        from application.apps.windows import DeviceSettingWindow
        app = DeviceSettingWindow(AppConfig("设备信息", "#f0f0f0", False, "500x170"))
        app.loadLabel(LabelConfig("设备标识", font_2, w=100, h=25, x=10, y=10))
        app.loadLabel(LabelConfig("手机型号", font_2, w=100, h=25, x=10, y=50))
        app.loadLabel(LabelConfig("系统版本", font_2, w=100, h=25, x=250, y=50))
        app.loadLabel(LabelConfig("应用名称", font_2, w=100, h=25, x=10, y=90))
        app.loadLabel(LabelConfig("应用版本", font_2, w=100, h=25, x=250, y=90))

        app.loadEntry("BilibiliBuvid_entry", EntryConfig(None, font_1, w=300, h=30, x=120, y=10))
        app.loadEntry("AndroidModel_entry", EntryConfig(None, font_1, w=120, h=30, x=120, y=50))
        app.loadEntry("AndroidBuild_entry", EntryConfig(None, font_1, w=120, h=30, x=360, y=50))
        app.loadEntry("VersionName_entry", EntryConfig(None, font_1, w=120, h=30, x=120, y=90))
        app.loadEntry("VersionCode_entry", EntryConfig(None, font_1, w=120, h=30, x=360, y=90))

        from application.module.command.setting import (
            DeviceSettingCommandRandom as Func4Random,
            DeviceSettingCommandApply as Func4Apply
        )

        app_args = (Func4Apply, ButtonConfig("应用/保存", font_0, w=460, h=30, x=20, y=130))
        app.loadButton(Func4Random, ButtonConfig("随机", font_0, w=50, h=30, x=430, y=10))
        app.loadButton(*app_args, main_app_root=self.root)

        # 写入
        devices = get_all_device_value(self.root, False)
        for li in devices:
            app[f"{li}_entry"].writer(devices[li])

        # 自动获取
        if not devices["VersionName"] or not devices["VersionCode"]:
            code, name = get_versions("android")
            app["VersionCode_entry"].writer(str(code))
            app["VersionName_entry"].writer(str(name))
