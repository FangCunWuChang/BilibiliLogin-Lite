from application.utils import reader

default_net_config = reader("./settings/net/default.json")
login_config = reader("./settings/net/login.json")
for li in login_config.copy():
    lili = login_config[li]
    lili.update(login_config["main"])
    login_config[li] = lili

main_button_settings = reader("./settings/controls/main/button.json")

setting_label_settings = reader("./settings/controls/setting/label.json")
setting_entry_settings = reader("./settings/controls/setting/entry.json")
setting_button_settings = reader("./settings/controls/setting/button.json")

sms_login_label_settings = reader("./settings/controls/sms_login/label.json")
sms_login_entry_settings = reader("./settings/controls/sms_login/entry.json")
sms_login_button_settings = reader("./settings/controls/sms_login/button.json")


password_login_label_settings = reader("./settings/controls/password_login/label.json")
password_login_entry_settings = reader("./settings/controls/password_login/entry.json")
password_login_button_settings = reader("./settings/controls/password_login/button.json")


password_verify_label_settings = reader("./settings/controls/password_verify/label.json")
password_verify_entry_settings = reader("./settings/controls/password_verify/entry.json")
password_verify_button_settings = reader("./settings/controls/password_verify/button.json")


chromedriver_index_url = reader("./settings/net/chromedriver.json").get("url")
chromedriver_download_url = reader("./settings/net/chromedriver.json").get("url2")
