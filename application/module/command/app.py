from application.module.utils import (
    ButtonCommand,
    get_all_device_value
)
from application.module.decoration import (
    application_error,
    application_thread
)
from application.apps.windows import (
    SmsLoginWindow,
    PasswordLoginWindow,
    DeviceSettingWindow
)
from application.config import (
    config_base_SmsLogin,
    config_base_PasswordLogin,
    config_base_DeviceSetting
)
from application.config import (
    config_controls_SmsLogin_login_button,
    config_controls_SmsLogin_send_button,

    config_controls_SmsLogin_cid_entry,
    config_controls_SmsLogin_code_entry,
    config_controls_SmsLogin_tel_entry,

    config_controls_SmsLogin_cid_label,
    config_controls_SmsLogin_tel_label,
    config_controls_SmsLogin_code_label,
)
from application.config import (
    config_controls_PasswordLogin_login_button,

    config_controls_PasswordLogin_password_entry,
    config_controls_PasswordLogin_username_entry,

    config_controls_PasswordLogin_password_label,
    config_controls_PasswordLogin_username_label,
)
from application.config import (
    config_controls_DeviceSetting_apply_button,
    config_controls_DeviceSetting_random_button,

    config_controls_DeviceSetting_buvid_entry,
    config_controls_DeviceSetting_code_entry,
    config_controls_DeviceSetting_name_entry,
    config_controls_DeviceSetting_model_entry,
    config_controls_DeviceSetting_osver_entry,

    config_controls_DeviceSetting_buvid_label,
    config_controls_DeviceSetting_code_label,
    config_controls_DeviceSetting_name_label,
    config_controls_DeviceSetting_model_label,
    config_controls_DeviceSetting_osver_label,
)
from application.module.command.login import (
    SmsLoginCommandSendVerifyCode,
    SmsLoginCommandLoginSms,
    PasswordLoginCommandOauth2
)
from application.module.command.setting import (
    DeviceSettingCommandRandom,
    DeviceSettingCommandApply
)
from application.net.utils import get_versions


class AppCommandSmsLogin(ButtonCommand):
    def __init__(self, *args, **kwargs):
        super(AppCommandSmsLogin, self).__init__(*args, **kwargs)

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        device = get_all_device_value(self.root)
        app = SmsLoginWindow(config_base_SmsLogin, device)
        app.loadLabel(config_controls_SmsLogin_cid_label)
        app.loadLabel(config_controls_SmsLogin_tel_label)
        app.loadLabel(config_controls_SmsLogin_code_label)
        app.loadEntry("tel_entry", config_controls_SmsLogin_tel_entry)
        app.loadEntry("cid_entry", config_controls_SmsLogin_cid_entry)
        app.loadEntry("code_entry", config_controls_SmsLogin_code_entry)
        app.loadButton(SmsLoginCommandSendVerifyCode, config_controls_SmsLogin_send_button)
        app.loadButton(SmsLoginCommandLoginSms, config_controls_SmsLogin_login_button)


class AppCommandPasswordLogin(ButtonCommand):
    def __init__(self, *args, **kwargs):
        super(AppCommandPasswordLogin, self).__init__(*args, **kwargs)

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        device = get_all_device_value(self.root)
        app = PasswordLoginWindow(config_base_PasswordLogin, device)
        app.loadLabel(config_controls_PasswordLogin_password_label)
        app.loadLabel(config_controls_PasswordLogin_username_label)
        app.loadEntry("password_entry", config_controls_PasswordLogin_password_entry)
        app.loadEntry("username_entry", config_controls_PasswordLogin_username_entry)
        app.loadButton(PasswordLoginCommandOauth2, config_controls_PasswordLogin_login_button)


class AppCommandDeviceSetting(ButtonCommand):
    def __init__(self, *args, **kwargs):
        super(AppCommandDeviceSetting, self).__init__(*args, **kwargs)

    @application_thread
    @application_error
    def func(self):
        print(self.__class__)

        app = DeviceSettingWindow(config_base_DeviceSetting)
        app.loadLabel(config_controls_DeviceSetting_buvid_label)
        app.loadLabel(config_controls_DeviceSetting_code_label)
        app.loadLabel(config_controls_DeviceSetting_name_label)
        app.loadLabel(config_controls_DeviceSetting_model_label)
        app.loadLabel(config_controls_DeviceSetting_osver_label)
        app.loadEntry("BilibiliBuvid_entry", config_controls_DeviceSetting_buvid_entry)
        app.loadEntry("AndroidModel_entry", config_controls_DeviceSetting_model_entry)
        app.loadEntry("AndroidBuild_entry", config_controls_DeviceSetting_osver_entry)
        app.loadEntry("VersionName_entry", config_controls_DeviceSetting_name_entry)
        app.loadEntry("VersionCode_entry", config_controls_DeviceSetting_code_entry)
        app.loadButton(DeviceSettingCommandRandom, config_controls_DeviceSetting_random_button)
        app_args = (DeviceSettingCommandApply, config_controls_DeviceSetting_apply_button)
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
