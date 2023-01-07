import tkinter

from application.utils import read_device_content
from application.errors import GuiItemNotExist
from application.items import (
    TkinterEntry,
    TkinterLabel
)
from application.config import (
    config_base_app,
    config_controls_app_SmsLogin_button,
    config_controls_app_PasswordLogin_button,
    config_controls_app_SettingDevice_button
)
from application.module.command.app import (
    AppCommandSmsLogin,
    AppCommandPasswordLogin,
    AppCommandDeviceSetting
)
from application.items import (
    ButtonConfig,
    LabelConfig,
    AppConfig,
    EntryConfig
)


class App(tkinter.Tk):
    def __init__(self, config: AppConfig):
        super(App, self).__init__()

        self.title(config.title)
        self.configure(background=config.bg)
        self.resizable(*config.resizable)
        self.geometry(config.geometry)

    def __setitem__(self, key: str, value) -> any:
        """ 设置 """
        return setattr(self, str(key), value)

    def __getitem__(self, item: str):
        """ 取得 """
        value = getattr(self, str(item), None)
        if value is None:
            raise GuiItemNotExist(f"找不到{item}")
        return value

    def loadButton(self, command: any, config: ButtonConfig):
        command(self, config)

    def loadEntry(self, item_name: str, config: EntryConfig):
        self[item_name] = TkinterEntry(self, config=config)

    def loadLabel(self, config: LabelConfig):
        TkinterLabel(self, config=config)


device_content = read_device_content()

app = App(config_base_app)

app["Device_BilibiliBuvid"] = device_content.get("BilibiliBuvid", "")
app["Device_AndroidModel"] = device_content.get("AndroidModel", "")
app["Device_AndroidBuild"] = device_content.get("AndroidBuild", "")
app["Device_VersionName"] = device_content.get("VersionName", "")
app["Device_VersionCode"] = device_content.get("VersionCode", "")

app.loadButton(AppCommandSmsLogin, config_controls_app_SmsLogin_button)
app.loadButton(AppCommandPasswordLogin, config_controls_app_PasswordLogin_button)
app.loadButton(AppCommandDeviceSetting, config_controls_app_SettingDevice_button)
