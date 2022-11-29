from application.apps.windows.app import TopWindow

from application.config import (
    setting_label_settings,
    setting_entry_settings,
    setting_button_settings
)

from application.module.controls import (
    TkinterLabel,
    TkinterEntry,
    TkinterButton
)

from application.module.command.setting import random_buvid, save_apply
from application.utils import get_all_value

from functools import partial


setting_func_list = [
    ("random", random_buvid),
    ("apply", save_apply)
]


class SettingDeviceWindow(TopWindow):
    def __init__(self, master):
        super(SettingDeviceWindow, self).__init__("设备信息", "500x170")

        self.main_master = master

        for label_config in setting_label_settings:
            TkinterLabel(self, label_config)

        for name, config in setting_entry_settings.items():
            self[f"{name}_entry"] = TkinterEntry(self, config)

        device = get_all_value(master, "Device_", [], True)
        for name, value in device.items():
            self[f"{name}_entry"].writer(value)

        for name, func in setting_func_list:
            config = setting_button_settings[name]
            TkinterButton(self, config, partial(func, self))
