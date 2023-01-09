import tkinter
import time

from application.errors import (
    GuiItemNotExist,
    DidNotEnter,
    VerifyCodeFormatError,
)
from application.module.decoration import (
    application_thread,
    application_error
)
from application.items import (
    AppConfig,
    ButtonConfig,
    EntryConfig,
    LabelConfig,
    ProgressbarConfig
)
from application.items import (
    TkinterEntry,
    TkinterLabel,
    TkinterButton,
    TkinterProgressbar
)
from application.net.utils import download_chromedriver
from application.config import font_1


class ProgressWindow(tkinter.Tk):
    def __init__(self, version: str):
        super(ProgressWindow, self).__init__()

        self.title("download chromedriver.exe")
        self.configure(background="#f0f0f0")
        self.resizable(False, False)
        self.geometry("300x50")

        config = ProgressbarConfig(100, 0, w=280, h=30, x=10, y=10)
        self.progressbar = TkinterProgressbar(self, config)

        self.chromedriver_file_zip = "./chromedriver.zip"

        self.func(version)

    def wait_show(self, t: int = 10):
        while not self.winfo_exists():
            time.sleep(t / 1000)

    @application_thread
    @application_error
    def func(self, version: str) -> None:
        self.wait_show()

        res, length = download_chromedriver(version)
        content_length = 0
        with open(self.chromedriver_file_zip, "wb") as f:
            for content in res.iter_content(1024):
                f.write(content)
                content_length += len(content)

                up_length = round(content_length / length * 100)
                self.progressbar.up(up_length)
        f.close()
        res.close()
        self.destroy()


class InputWindow(tkinter.Tk):
    """ 输入窗口 """
    def __init__(self):
        super(InputWindow, self).__init__()
        self.title("输入验证码")
        self.configure(background="#f0f0f0")
        self.resizable(False, False)
        self.geometry("180x50")

        config1 = EntryConfig(None, font_1, w=100, h=30, x=10, y=10)
        config2 = ButtonConfig("提交", font_1, w=50, h=30, x=120, y=10)

        self.input_entry = TkinterEntry(self, config1)
        TkinterButton(self, config2, self.func)

        self.verify_code = None

    @application_thread
    @application_error
    def func(self) -> None:
        verify_code = self.input_entry.value()
        verify_code = verify_code.replace(" ", "")
        if not verify_code:
            raise DidNotEnter("未输入验证码")
        if not verify_code.isdigit():
            raise VerifyCodeFormatError("验证码不能带有字符串")
        if len(verify_code) != 6:
            raise VerifyCodeFormatError("验证码长度错误")
        self.verify_code = verify_code
        self.destroy()


class TopWindow(tkinter.Toplevel):
    """ 子窗口 """
    def __init__(self, config: AppConfig):
        super(TopWindow, self).__init__()

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

    def loadButton(self, command: any, config: ButtonConfig, **kwargs):
        command(self, config, **kwargs)

    def loadEntry(self, item_name: str, config: EntryConfig):
        self[item_name] = TkinterEntry(self, config=config)

    def loadLabel(self, config: LabelConfig):
        TkinterLabel(self, config=config)
