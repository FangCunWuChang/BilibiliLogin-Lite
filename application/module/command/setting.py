from application.utils import get_all_value, writer

from application.module.decoration import (
    application_error, application_thread
)

import uuid


@application_thread
@application_error
def random_buvid(master) -> None:
    random_text = str(uuid.uuid4()).replace("-", "")
    while len(random_text) < 35:
        random_text += str(uuid.uuid4()).replace("-", "")
    fake_buvid = str("XY" + random_text[:35]).upper()
    master["Buvid_entry"].writer(fake_buvid)


@application_thread
@application_error
def save_apply(master) -> None:
    device_dict = get_all_value(master, "_entry", [])
    for name, value in device_dict.items():
        master.main_master[f"Device_{name}"] = value

    writer("./device.json", device_dict)
