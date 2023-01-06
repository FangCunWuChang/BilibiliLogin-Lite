
class GuiItemNotExist(Exception):
    """ [错误]GUI无法取得值 """
    def __init__(self, *args):
        super(GuiItemNotExist, self).__init__(*args)
        self.title = "GUI无法取得值"


class GuiDeviceValueNotExist(Warning):
    """ [警告]设备信息未填写 """
    def __init__(self, *args):
        super(GuiDeviceValueNotExist, self).__init__(*args)
        self.title = "[警告]设备信息未填写"


class DidNotEnter(Warning):
    """ [警告]未输入内容 """
    def __init__(self, *args):
        super(DidNotEnter, self).__init__(*args)
        self.title = "[警告]未输入内容"


class TelNumberFormatError(Warning):
    """ [警告]手机号格式不正确 """
    def __init__(self, *args):
        super(TelNumberFormatError, self).__init__(*args)
        self.title = "[警告]手机号格式不正确"


class CidFormatError(Warning):
    """ [警告]区号格式不正确 """
    def __init__(self, *args):
        super(CidFormatError, self).__init__(*args)
        self.title = "[警告]区号格式不正确"


class VerifyCodeFormatError(Warning):
    """ [警告]验证码格式不正确 """
    def __init__(self, *args):
        super(VerifyCodeFormatError, self).__init__(*args)
        self.title = "[警告]验证码格式不正确"


class ReaderError(Exception):
    """ [错误]无法读取 """
    def __init__(self, *args):
        super(ReaderError, self).__init__(*args)
        self.title = "[错误]无法读取"


class GuiFileAskWarning(Warning):
    """ [警告]未打开文件会话 """
    def __init__(self, *args: object):
        super(GuiFileAskWarning, self).__init__(*args)
        self.title = "[警告]未打开文件会话"


class SdkIntIndexError(Exception):
    """ [错误]无法找到对应的SdkInt"""
    def __init__(self, *args: object):
        super(SdkIntIndexError, self).__init__(*args)
        self.title = "[错误]无法找到对应的SdkInt"


class ResponseError(Exception):
    """ [错误]响应错误 """
    def __init__(self, *args: object):
        super(ResponseError, self).__init__(*args)
        self.title = "[错误]响应错误"


class ChromedriverUpgradeError(Exception):
    """ [错误]chromedriver自动更新错误 """
    def __init__(self, *args):
        super(ChromedriverUpgradeError, self).__init__(*args)
        self.title = "[错误]chromedriver自动更新错误"
