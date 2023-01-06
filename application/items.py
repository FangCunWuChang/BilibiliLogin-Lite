import tkinter


from application.config import (
    EntryConfig, ButtonConfig, LabelConfig
)


class TkinterEntry(tkinter.Entry):
    """ 输入框 """
    def __init__(self, root, config: EntryConfig):
        super(TkinterEntry, self).__init__(root, **config.content)
        self.insert(0, config.default or "")
        self.place(**config.place)

    def writer(self, text: str):
        """ 显示 """
        self.delete(0, tkinter.END)
        self.insert(0, text or str())

    def value(self):
        """ 获取内容 string err 不存在则抛出异常 """
        return str(self.get())

    def number(self, f=True) -> float | int:
        """ 获取内容 !f = int """
        value = self.value()
        if not value:
            return 0. if f else 0
        negative = False
        if value[:1] == "-":
            negative = True
            value = value[1:]
        if value.isdigit():
            number = float(value)
            res = number if f else round(number)
            return res * -1 if negative else res
        s = value.split(".")
        if 0 < len(s) <= 2:
            while "" in s:
                s.remove("")
            if all([i.isdigit() for i in s]):
                number = float(value)
                res = number if f else round(number)
                return res * -1 if negative else res
        return 0. if f else 0


class TkinterLabel(tkinter.Label):
    """ 标签 """
    def __init__(self, root, config: LabelConfig):
        super(TkinterLabel, self).__init__(root, **config.content)
        self.place(**config.place)


class TkinterButton(tkinter.Button):
    """ 按钮 """
    def __init__(self, root, config: ButtonConfig, func: any):
        root_config = config.content
        root_config.update({"command": func})
        super(TkinterButton, self).__init__(root, **root_config)
        self.place(**config.place)
