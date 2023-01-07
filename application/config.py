from application.utils import reader

from application.items import (
    AppConfig,
    ButtonConfig,
    LabelConfig,
    EntryConfig
)


font_0 = ("Microsoft YaHei", 14)
font_1 = ("Microsoft YaHei", 16)
font_2 = ("Microsoft YaHei", 18)


# "主页面"基础样式
config_base_app = AppConfig("登陆", "#f0f0f0", False, "200x130")

# "短信登陆"基础样式
config_base_SmsLogin = AppConfig("短信登陆", "#f0f0f0", False, "300x130")

# "账密登陆"基础样式
config_base_PasswordLogin = AppConfig("账密登陆", "#f0f0f0", False, "300x130")

# "设备信息"基础样式
config_base_DeviceSetting = AppConfig("设备信息", "#f0f0f0", False, "500x170")

# "主页面"页面样式
config_controls_app_SmsLogin_button = ButtonConfig("短信登陆", font_0, w=180, h=30, x=10, y=10)
config_controls_app_PasswordLogin_button = ButtonConfig("账密登陆", font_0, w=180, h=30, x=10, y=50)
config_controls_app_SettingDevice_button = ButtonConfig("设备信息", font_0, w=180, h=30, x=10, y=90)


# "短信登陆(app)"页面样式
config_controls_SmsLogin_tel_entry = EntryConfig(None, font_1, w=185, h=30, x=100, y=10)
config_controls_SmsLogin_code_entry = EntryConfig(None, font_1, w=105, h=30, x=100, y=50)
config_controls_SmsLogin_cid_entry = EntryConfig("86", font_1, w=50, h=30, x=100, y=90)

config_controls_SmsLogin_send_button = ButtonConfig("发送", font_0, w=65, h=30, x=220, y=50)
config_controls_SmsLogin_login_button = ButtonConfig("登陆", font_0, w=125, h=30, x=160, y=90)

config_controls_SmsLogin_tel_label = LabelConfig("手机号", font_2, w=75, h=30, x=10, y=10)
config_controls_SmsLogin_code_label = LabelConfig("验证码", font_2, w=75, h=30, x=10, y=50)
config_controls_SmsLogin_cid_label = LabelConfig("地区号", font_2, w=75, h=30, x=10, y=90)


# "密码登陆(app)"页面样式
config_controls_PasswordLogin_username_entry = EntryConfig(None, font_1, w=210, h=30, x=75, y=10)
config_controls_PasswordLogin_password_entry = EntryConfig(None, font_1, w=210, h=30, x=75, y=50)

config_controls_PasswordLogin_login_button = ButtonConfig("登陆", font_0, w=280, h=30, x=10, y=90)

config_controls_PasswordLogin_username_label = LabelConfig("账号", font_2, w=50, h=30, x=10, y=10)
config_controls_PasswordLogin_password_label = LabelConfig("密码", font_2, w=50, h=30, x=10, y=50)

# "设备信息设置"页面样式
config_controls_DeviceSetting_buvid_entry = EntryConfig(None, font_1, w=300, h=30, x=120, y=10)
config_controls_DeviceSetting_model_entry = EntryConfig(None, font_1, w=120, h=30, x=120, y=50)
config_controls_DeviceSetting_osver_entry = EntryConfig(None, font_1, w=120, h=30, x=360, y=50)
config_controls_DeviceSetting_name_entry = EntryConfig(None, font_1, w=120, h=30, x=120, y=90)
config_controls_DeviceSetting_code_entry = EntryConfig(None, font_1, w=120, h=30, x=360, y=90)

config_controls_DeviceSetting_random_button = ButtonConfig("随机", font_0, w=50, h=30, x=430, y=10)
config_controls_DeviceSetting_apply_button = ButtonConfig("应用/保存", font_0, w=460, h=30, x=20, y=130)

config_controls_DeviceSetting_buvid_label = LabelConfig("设备标识", font_2, w=100, h=25, x=10, y=10)
config_controls_DeviceSetting_model_label = LabelConfig("手机型号", font_2, w=100, h=25, x=10, y=50)
config_controls_DeviceSetting_osver_label = LabelConfig("系统版本", font_2, w=100, h=25, x=250, y=50)
config_controls_DeviceSetting_name_label = LabelConfig("应用名称", font_2, w=100, h=25, x=10, y=90)
config_controls_DeviceSetting_code_label = LabelConfig("应用版本", font_2, w=100, h=25, x=250, y=90)

# 登陆网络设置
login_config = reader("./settings/net/login.json")
for li in login_config.copy():
    lili = login_config[li]
    lili.update(login_config["main"])
    login_config[li] = lili
default_net_config = reader("./settings/net/default.json")


# chromedriver链接
chromedriver_index_url = "https://registry.npmmirror.com/-/binary/chromedriver/"
chromedriver_download_url = "https://cdn.npmmirror.com/binaries/chromedriver/{VERSION}/chromedriver_win32.zip"

chromedriver_file = "geetest/chromedriver.exe"

# 登陆所需密钥
LOGIN_SIGN_Android = ("783bbb7264451d82", "2653583c8873dea268ab9386918b1d65")
