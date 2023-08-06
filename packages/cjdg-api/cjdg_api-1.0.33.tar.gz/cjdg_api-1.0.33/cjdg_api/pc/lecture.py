from requests.api import delete
from ..base import base
from loguru import logger


class lecture(base):
    url = "https://client.chaojidaogou.com/allstar/api/lecture/"

    def __init__(self, token):
        super().__init__(token)

    def list(self):
        pass

    def read(self, id):
        pass

    def update(self, data):
        pass

    def delete(self, id):
        pass

    def create(self, userIds, flag=0, tagIds=941, des=""):
        url = f"{self.url}addUserAsLecturer"
        params = {
            "userIds": userIds,
            "flag": flag,
            "tagIds": tagIds,
            "des": des,
        }
        return self.request(
            url=url,
            params=params,
            method="POST"
        )
