import tkinter

from application.utils import read_device_content
from application.errors import GuiItemNotExist
from application.config import font_0
from application.items import (
    TkinterEntry,
    TkinterLabel,
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


def load_app() -> App:
    """ 加载应用 """
    app = App(AppConfig("登陆", "#f0f0f0", False, "200x130"))

    device_content = read_device_content()

    app["Device_BilibiliBuvid"] = device_content.get("BilibiliBuvid", "")
    app["Device_AndroidModel"] = device_content.get("AndroidModel", "")
    app["Device_AndroidBuild"] = device_content.get("AndroidBuild", "")
    app["Device_VersionName"] = device_content.get("VersionName", "")
    app["Device_VersionCode"] = device_content.get("VersionCode", "")

    from application.module.command.app import (
        AppCommandSmsLogin as Func4SmsLogin,
        AppCommandPasswordLogin as Func4PasswordLogin,
        AppCommandDeviceSetting as Func4DeviceSetting
    )

    app.loadButton(Func4SmsLogin, ButtonConfig("短信登陆", font_0, w=180, h=30, x=10, y=10))
    app.loadButton(Func4PasswordLogin, ButtonConfig("账密登陆", font_0, w=180, h=30, x=10, y=50))
    app.loadButton(Func4DeviceSetting, ButtonConfig("设备信息", font_0, w=180, h=30, x=10, y=90))

    return app
