import requests


class Session:
    def __init__(self, host: str, token: str, repo: str):
        self.repo = repo
        self.__host = host
        self._session = requests.Session()
        self._session.headers.update({
            'Authorization': f'Bearer {token}'
        })

    def get(self, url: str, add_repo: bool = True):
        host = f"{self.__host}/repos/{self.repo}" if add_repo else self.__host
        return self._session.get(f"{host}{url}").json()

    def post(self, url: str, data: dict = None, add_repo: bool = True):
        host = f"{self.__host}/repos/{self.repo}" if add_repo else self.__host
        return self._session.post(f"{host}{url}", data=data).json()

    def delete(self, url: str, add_repo: bool = True):
        host = f"{self.__host}/repos/{self.repo}" if add_repo else self.__host
        return self._session.delete(f"{host}{url}")

    def patch(self, url: str, data: dict = None, add_repo: bool = True):
        host = f"{self.__host}/repos/{self.repo}" if add_repo else self.__host
        return self._session.patch(f"{host}{url}", data=data).json()
