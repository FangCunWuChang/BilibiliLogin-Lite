from requests.utils import cookiejar_from_dict
import requests


class Session(requests.Session):
    def __init__(self, **kwargs):
        super(Session, self).__init__()
        __cookies = kwargs.get("cookies", dict())

        self.trust_env = kwargs.get("trust_env", False)
        self.proxies = kwargs.get("proxies", None)
        self.headers.update(kwargs.get("headers", dict()))
        self.cookies = cookiejar_from_dict(__cookies)
