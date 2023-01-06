from application.errors import ReaderError


from urllib.parse import urlsplit
from urllib.parse import unquote
import base64
import json
import uuid
import rsa
import os


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


def read_device_content():
    """ 打开device.json """
    default_device_file = "./device.json"
    if os.path.exists(default_device_file):
        return reader(default_device_file)
    return dict()


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


def urlQuerySplit(url: str) -> dict:
    """ 分割url query参数 """
    data: list[str] = urlsplit(url).query.split("&")
    query_dict = dict()
    for li in data:
        i = li.split("=")
        query_dict[i[0]] = "" if len(i) == 1 else unquote(i[1])
    return query_dict


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
