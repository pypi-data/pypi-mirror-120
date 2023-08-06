from typing import TypedDict
import requests

class QueryDict(TypedDict):
    title: str
    file_name: str
    visibility: str

class GistItem(TypedDict):
    id: int
    title: str
    file_name: str
    visibility: str
    web_url: str


class Gist(object):
    def __init__(self, username: str, password: str, api: str) -> None:
        self.api = api.strip(' /')
        self.username = username
        self.password = password
        self.access_token = None

    def validate_api(self):
        """校验api是否有效，并执行oauth认证"""
        try:
            # 1. 尝试获取版本，确保API是否正确
            rsp = requests.get(f"{self.api}/api/v4/version")
        except Exception as e:
            raise RuntimeError("gitlab地址无效，无法获取gitlab api版本信息")

        if rsp.status_code == 401:
            self.oauth()
        rsp = requests.get(f"{self.api}/api/v4/version?access_token={self.access_token}")
        if rsp.status_code == 401:
            raise RuntimeError("认证信息无效：" + rsp.reason)

    def oauth(self):
        """发起oauth2认证，获取accesss_token
        """
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password
        }
        rsp = requests.post(f"{self.api}/oauth/token", data=data)
        d = rsp.json()
        if d.get('access_token'):
            self.access_token = d['access_token']
        else:
            raise RuntimeError("获取Access_token失败:" + d.get("error"))

    def create(self, title: str, file_name: str, content: str, visibility: str = 'private', description: str = "") -> GistItem:
        data = {
            "title": title,
            "file_name": file_name,
            "content": content,
            "description": description,
            "visibility": visibility
        }
        if not self.access_token:
            raise RuntimeError("No Access Token!!!")
        api = f"{self.api}/api/v4/snippets?access_token={self.access_token}"
        rsp = requests.post(api, json=data)
        return rsp.json()

    def update(self, snippet: GistItem, content: str) -> GistItem:
        api = f"{self.api}/api/v4/snippets/{snippet['id']}?access_token={self.access_token}"
        rsp = requests.put(api, json={"content": content})
        return rsp.json()

    def query(self, filter: QueryDict) -> list[GistItem]:
        rsp = requests.get(f'{self.api}/api/v4/snippets?access_token={self.access_token}')
        datas: list[dict] = rsp.json()

        items = []
        for data in datas:
            if all([data[k] == filter[k] for k in filter]):
                items.append(data)

        return items

    def get_content(self, gist_id: str) -> str:
        rsp = requests.get(f'{self.api}/api/v4/snippets/{gist_id}/raw?access_token={self.access_token}')
        return rsp.text