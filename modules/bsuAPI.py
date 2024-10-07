import requests
from bs4 import BeautifulSoup as BS


class BSU:

    class object:

        def __init__(self, username, password, href) -> None:
            self._UUID = 0
            self._is_auth = False
            self._session = requests.Session()
            self._site = str(self._session.get(f'https://{href}').content.decode('utf-8'))
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
            site = self._session.get(location, data={"testsession": self._UUID})
            logininfo = BS(str(site.content), 'lxml').find('div', class_='logininfo').find_all('a')
            self.fio = logininfo[0].text
            href = logininfo[1]['href']
            self._session_key = href[href.find('=')+1:]

    class dekanat(object):

        white_list = [
            'Календарь посещаемости занятий',
            'Зачётная книжка',
            'Электронные услуги'
        ]

        def __init__(self, username, password):
            super().__init__(username, password, 'dekanat.bsu.edu.ru/login/index.php')
            location, self._UUID = self.auth('https://dekanat.bsu.edu.ru/login/index.php')
            self.get_check_date(location)

        def get_function(self):
            site = self._session.get('https://dekanat.bsu.edu.ru').content.decode('utf-8')
            lis = BS(str(site), 'lxml').find('div', id='inst291').find_all('a')
            res = {}
            for data in lis:
                name = data.text.replace('\xa0', '')
                if name in self.white_list:
                    res[name] = data['href']
            print(res)

    class mail(object):
        def __init__(self, username, password):
            super().__init__(username, password, 'mail.bsu.edu.ru')
            tokens = BS(self._site, "lxml").find(
                'form',
                id='zLoginForm').find_all('input')
            self._PAYLOAD['loginOp'] = tokens[0]['value']
            self._PAYLOAD['login_csrf'] = tokens[1]['value']
            self._PAYLOAD['client'] = 'preferred'

    class pegas(object):
        def __init__(self, username, password):
            super().__init__(username, password, 'pegas.bsuedu.ru/login/index.php')
            with open('pegas_login.html', 'w') as file:
                file.write(self._site)
            self._PAYLOAD['logintoken'] = BS(self._site, 'lxml').find('form', class_='login-form').find('input', type='hidden')['value']
            location, self._UUID = self.auth('https://pegas.bsuedu.ru/login/index.php')
            self.get_check_date(location)

    def __init__(self, username, password):
        __session = requests.Session()
        __PAYLOAD = {
            "username": username,
            "password": password
        }
        self.__is_auth = False
        # Регистрация
        __session.get('https://dekanat.bsu.edu.ru')
        # Авторизация
        auth = __session.post(
            "https://dekanat.bsu.edu.ru/login/index.php",
            data=__PAYLOAD,
            allow_redirects=False)
        match auth.status_code:
            case 303:
                self._dekanat = self.dekanat(username, password)
                # self._mail = self.mail(username, password)
                self._pegas = self.pegas(username, password)
            case 200:
                print("Неверно введён логин и пароль")
            case _:
                print(f'Не обрабатываемый код запроса: {auth.status_code}')
