import requests
from bs4 import BeautifulSoup as BS


class element:

    def __init__(self, username, password, href) -> None:
        self._UUID = 0
        self._is_auth = False
        self._session = requests.Session()
        self._site = str(self._session.get(
            f'https://{href}').content.decode('utf-8'))
        self._PAYLOAD = {
            "username": username,
            "password": password
        }

    def get_html(self, name, site):
        with open(f'{name}.html', 'w') as file:
            file.write(site)

    def auth(self, href, allow_redirects=False):
        auth = self._session.post(
            href,
            data=self._PAYLOAD,
            allow_redirects=allow_redirects)
        location = auth.headers.pop('Location')
        session_id = location[location.find('=')+1:]
        return location, session_id

    def get_check_date(self, location) -> None:
        # Проверка
        site = self._session.get(
            location,
            data={"testsession": self._UUID})
        logininfo = BS(str(site.content), 'lxml').find(
            'div',
            class_='logininfo').find_all('a')
        self.fio = logininfo[0].text
        href = logininfo[1]['href']
        self._session_key = href[href.find('=')+1:]

    def get_decode_BS(self, href) -> BS:
        site = str(self._session.get(href).content.decode('utf-8'))
        return BS(site, 'lxml')
