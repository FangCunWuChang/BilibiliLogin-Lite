from application.apps.utils import TopWindow
from application.config import AppConfig


class SmsLoginWindow(TopWindow):
    """ 短信登陆窗口 """
    def __init__(self, config: AppConfig, device: dict):
        super(SmsLoginWindow, self).__init__(config)
        self.device = device
        self.captcha_key = None


class PasswordLoginWindow(TopWindow):
    """ 账密登陆窗口 """
    def __init__(self, config: AppConfig, device: dict):
        super(PasswordLoginWindow, self).__init__(config)
        self.device = device


class DeviceSettingWindow(TopWindow):
    """ 设备信息窗口 """
    def __init__(self, config: AppConfig):
        super(DeviceSettingWindow, self).__init__(config)
