from modules.object import element

from bs4 import BeautifulSoup as BS


class pegas(element):

    def __init__(self, username, password):
        super().__init__(username, password,
                         'pegas.bsuedu.ru/login/index.php')
        self._PAYLOAD['logintoken'] = BS(self._site, 'lxml').find(
            'form',
            class_='login-form').find('input', type='hidden')['value']
        location, self._UUID = self.auth(
            'https://pegas.bsuedu.ru/login/index.php')
        self.get_check_date(location)
