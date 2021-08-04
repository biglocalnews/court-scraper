import requests
from fake_useragent import UserAgent


class RequestsBasePage:

    def get_html(self, url, payload=None, fakeuser=None):
        self.url = url
        if fakeuser:
            fakeuser = UserAgent()
            headers = {'user-agent': fakeuser.chrome}
            data = requests.get(url, headers=headers, params=payload)
        else:
            data = requests.get(url, params=payload)
        return data

    def save_html(self, data, filename):
        self.file = open(filename, "a")
        self.file.write(data)
        self.file.close()
