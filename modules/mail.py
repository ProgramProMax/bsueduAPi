from bs4 import BeautifulSoup as BS

from modules.object import element


class mail(element):
    def __init__(self, username, password):
        super().__init__(username, password, 'mail.bsu.edu.ru')
        tokens = BS(self._site, "lxml").find(
            'form',
            id='zLoginForm').find_all('input')
        self._PAYLOAD['loginOp'] = tokens[0]['value']
        self._PAYLOAD['login_csrf'] = tokens[1]['value']
        self._PAYLOAD['client'] = 'preferred'
