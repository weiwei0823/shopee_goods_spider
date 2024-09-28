import json

import requests


class AdsBrowser:
    def __init__(self, index=0):
        self.api_key = "343dc04953e2d3d6d89346ed8fd70608"
        self.username = "liudewei0616@gmail.com"
        self.password = "Qww870823"
        self.base_url = "http://local.adspower.net:50325"
        self.name = "ads_browser"
        self.group_id = 0
        self.proxy = {
            "type": "http",
            "host": "127.0.0.1",
            "port": "2022"
        }
        self.protocol = "http",
        self.domain_name = "https://www.bigseller.com/zh_CN/login.htm",

    # 创建分组
    def create_group(self):
        url = f"{self.base_url}/api/v1/group/create"
        response = requests.post(
            url=url,
            data=json.dumps({
                "group_name": self.group_id
            })
        ).text
        print(response)

    # 查询环境
    def get_user_list(self):
        url = f"{self.base_url}/api/v1/user/list"
        response = requests.post(
            url=url
        ).text
        print(response)

    # 新建浏览器
    def create_browser(self):
        url = f"{self.base_url}/api/v1/user/create"
        response = requests.post(
            url=url,
            data=json.dumps({
                "username": self.username,
                "password": self.password,
                "name": self.name,
                "group_id": self.group_id,
                "user_proxy_config": {
                    "proxy_soft": "no_proxy",
                    "proxy_type": self.proxy.get("type"),
                    "proxy_host": self.proxy.get("host"),
                    "proxy_port": self.proxy.get("port")
                },
                "fingerprint_config": {
                    "webrtc": "forward"
                }
            })
        ).text
        print(response)


if __name__ == "__main__":
    ads_browser = AdsBrowser()
    ads_browser.create_browser()
