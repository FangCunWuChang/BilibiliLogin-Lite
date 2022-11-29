from application.apps.windows.app import TopWindow

from application.module.controls import (
    TkinterLabel, TkinterEntry, TkinterButton
)

from application.config import (
    sms_login_label_settings,
    sms_login_entry_settings,
    sms_login_button_settings,

    password_login_label_settings,
    password_login_entry_settings,
    password_login_button_settings,
)

from application.net.login import SmsLogin, PasswordLogin

from application.module.command.sms_login import (
    sms_send_verify_code, sms_login_login
)

from application.module.command.password_login import (
    password_login_login
)

from functools import partial


sms_login_func = [
    ("send_verify_code", sms_send_verify_code),
    ("login_login", sms_login_login)
]


class SmsLoginWindow(TopWindow):
    def __init__(self, versions, system, buvid):
        super(SmsLoginWindow, self).__init__("短信登陆", "300x130")

        self.captcha_key = None

        self.login = SmsLogin(versions, system, buvid)

        for label_config in sms_login_label_settings:
            TkinterLabel(self, label_config)

        for name, entry_config in sms_login_entry_settings.items():
            self[f"{name}_entry"] = TkinterEntry(self, entry_config)

        for name, func in sms_login_func:
            config = sms_login_button_settings[name]
            TkinterButton(self, config, partial(func, self, buvid))


password_login_func = [
    ("login_login", password_login_login)
]


class PasswordLoginWindow(TopWindow):
    def __init__(self, versions, system, buvid):
        super(PasswordLoginWindow, self).__init__("账密登陆", "300x130")

        self.login = PasswordLogin(versions, system, buvid)

        for label_config in password_login_label_settings:
            TkinterLabel(self, label_config)

        for name, entry_config in password_login_entry_settings.items():
            self[f"{name}_entry"] = TkinterEntry(self, entry_config)

        for name, func in password_login_func:
            config = password_login_button_settings[name]
            TkinterButton(self, config, partial(func, self, buvid))
