from application.utils import reader

# font
font_0 = ("Microsoft YaHei", 14)
font_1 = ("Microsoft YaHei", 16)
font_2 = ("Microsoft YaHei", 18)


# 登陆网络设置
login_config = reader("./settings/net/login.json")
for li in login_config.copy():
    lili = login_config[li]
    lili.update(login_config["main"])
    login_config[li] = lili

default_net_config = reader("./settings/net/default.json")


# chromedriver 链接
chromedriver_index_url = "https://registry.npmmirror.com/-/binary/chromedriver/"
chromedriver_download_url = "https://cdn.npmmirror.com/binaries/chromedriver/{VERSION}/chromedriver_win32.zip"

# chromedriver 位置
chromedriver_file = "geetest/chromedriver.exe"

# 登陆所需密钥
LOGIN_SIGN_Android = ("783bbb7264451d82", "2653583c8873dea268ab9386918b1d65")
