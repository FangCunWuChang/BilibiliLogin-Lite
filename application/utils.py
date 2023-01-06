from application.errors import ReaderError, GuiValueIndexWarning


from urllib.parse import urlencode
from urllib.parse import urlsplit
from urllib.parse import unquote
import hashlib
import base64
import json
import uuid
import rsa
import os


class FormData(dict):
    def __init__(self, *args, **kwargs):
        super(FormData, self).__init__(*args, **kwargs)

    @property
    def sorted(self):
        """ 排序 """
        return {k: self[k] for k in sorted(self)}

    def toSign(self, app: tuple[str, str]):
        """ 计算sign """
        appkey, appsec = app
        self.update({"appkey": appkey})
        form_data = self.sorted
        text = urlencode(form_data) + appsec
        hashlib_md5 = hashlib.md5()
        hashlib_md5.update(text.encode())
        sign = hashlib_md5.hexdigest()
        form_data.update({"sign": sign})

        print(form_data)

        return form_data


ReaderMode_Setting = "setting"
ReaderMode_Content = "content"


def reader(path: str, mode=ReaderMode_Setting) -> list | dict | bytes:
    assert os.path.exists(path), ReaderError(f"{path}不存在")
    assert os.path.isfile(path), ReaderError(f"{path}非文件")
    with open(os.path.abspath(path), "rb") as file:
        file_data = file.read()
    file.close()
    if mode == ReaderMode_Setting:
        return json.loads(file_data.decode())
    elif mode == ReaderMode_Content:
        return file_data
    raise ReaderError(f"{path}无法打开")


def writer(path: str, data: list | dict | bytes) -> str:
    """ 写入 """
    file_path, file = os.path.split(path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    write_data = data
    if isinstance(data, list) or isinstance(data, dict):
        write_data = json.dumps(data).encode()
    with open(path, "wb") as w_file:
        w_file.write(write_data)
    w_file.close()
    return os.path.abspath(path)


def get_all_value(master, wkey: str, no_items: list, reverse=False) -> dict:
    """
    获取所有内容
    no_items 不抛出异常的值
    reverse 反向选择 不抛出异常的值
    """
    entry_dict, return_dict = dict(), dict()
    for key, value in master.__dict__.items():
        if wkey in key:
            entry_dict[key.replace(wkey, "")] = value
    if reverse:
        reverse_no_items = list(entry_dict.keys())
        for li in no_items:
            reverse_no_items.remove(li)
        no_items = reverse_no_items
    for key, entry in entry_dict.items():
        err = False if key in no_items else f"{key}未填写"
        if "_entry" in wkey:
            return_dict[key] = entry.value(err)
        else:
            if entry is None and err:
                raise GuiValueIndexWarning(err)
            return_dict[key] = entry
    return return_dict


def extractCookie(response_json: dict, buvid) -> tuple[str, str]:
    """ 提取 accessKey 和 cookie """
    access_key = str(response_json["data"]["token_info"]["access_token"])
    cookie_list = response_json["data"]["cookie_info"]["cookies"]
    cookie_dict = {li["name"]: li["value"] for li in cookie_list}
    cookie_dict.update({"Buvid": str(buvid)})
    cookie_list = [f"{k}={v}" for k, v in cookie_dict.items()]
    return access_key, "; ".join(cookie_list)


LOGIN_SIGN = ("783bbb7264451d82", "2653583c8873dea268ab9386918b1d65")


def addSign(form_data: dict, key_and_sec=LOGIN_SIGN) -> dict:
    """ 添加sign """
    text = urlencode(form_data) + key_and_sec[1]
    hashlib_md5 = hashlib.md5()
    hashlib_md5.update(text.encode())
    form_data.update({"sign": hashlib_md5.hexdigest()})
    return form_data


def urlQuerySplit(url: str) -> dict:
    """ 分割url query参数 """
    data: list[str] = urlsplit(url).query.split("&")
    query_dict = dict()
    for li in data:
        i = li.split("=")
        query_dict[i[0]] = "" if len(i) == 1 else unquote(i[1])
    return query_dict


def sortedFormData(form_data: dict):
    """ 表单排序 """
    return_form_data = dict()
    form_data_keys = sorted(form_data)
    for key in form_data_keys:
        return_form_data[key] = form_data[key]
    return return_form_data


def parse_cookies(cookies_content: str) -> dict:
    """  把字符串格式的cookie转为dict格式 """
    c1: list = cookies_content.split("; ")
    c2 = [i.split("=") for i in c1]
    return {i[0]: i[1] for i in c2}


def rsaPassword(password: str, rsa_key: str, rsa_hash: str):
    """ rsa密码加密 """
    pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key.encode())
    rsa_password = str(rsa_hash + password).encode()
    encrypted_password = rsa.encrypt(rsa_password, pub_key)
    return base64.b64encode(encrypted_password).decode()


def build_x_bili_trace_id(sela_time: int) -> str:
    """ 生成 x-bili-trace-id """
    back6 = hex(round(sela_time / 256))
    front = str(uuid.uuid4()).replace("-", "")
    _data1 = front[6:] + back6[2:]
    _data2 = front[22:] + back6[2:]
    return f"{_data1}:{_data2}:0:0"
