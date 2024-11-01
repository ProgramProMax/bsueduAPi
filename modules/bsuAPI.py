from requests import Session as ses

from modules.shedule import shedule
from modules.mail import mail
from modules.pegas import pegas
from modules.dekanat import dekanat


class BSU:

    def __init__(self, username, password, number_group=None, dekanat_on=False, mail_on=False, pegas_on=False):
        session = ses()
        __PAYLOAD = {
            "username": username,
            "password": password
        }
        self.is_auth = False
        # Регистрация
        session.get('https://dekanat.bsu.edu.ru')
        # Авторизация
        auth = session.post(
            "https://dekanat.bsu.edu.ru/login/index.php",
            data=__PAYLOAD,
            allow_redirects=False)
        match auth.status_code:
            case 303:
                self.is_auth = True
                self._dekanat = dekanat(username, password) if dekanat_on else None
                self._mail = mail(username, password) if mail_on else None
                self._shedule = shedule(number_group) if number_group!=None else None
                self._pegas = pegas(username, password) if pegas_on else None
            case 200:
                print("Неверно введён логин и пароль")
            case _:
                print(f'Не обрабатываемый код запроса: {auth.status_code}')
