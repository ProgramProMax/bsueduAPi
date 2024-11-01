
from modules.object import element
# from bs4 import BeautifulSoup as BS


class dekanat(element):

    white_list = {
        'Календарь посещаемости занятий': 'was_calandery',
        'Зачётная книжка': 'report_book',
        'Электронные услуги': 'online_service'
    }

    colums = [
            'name',
            'semestr',
            'hours',
            'teacher',
            'ocenka',
            'date_ocenka'
            ]

    def __init__(self, username, password):
        super().__init__(username, password,
                         'dekanat.bsu.edu.ru/login/index.php')
        location, self._UUID = self.auth(
            'https://dekanat.bsu.edu.ru/login/index.php')
        self.get_check_date(location)

    def get_function(self):
        lis = self.get_decode_BS('https://dekanat.bsu.edu.ru/')
        res = {}
        for data in lis.find('div', id='inst291').find_all('a'):
            name = data.text.replace('\xa0', '')
            if name in self.white_list:
                res[self.white_list[name]] = data['href']
        self.funcs = res
        print(res)

    # Получение зачётки
    def get_report_card(self):
        print('Оценки')
        site = self.get_decode_BS(self.funcs['report_book']+'&term=20')
        res = []
        soup = site.find('div', class_='region-content')
        report_card = soup.find('div', id='plandisc')
        num_report_card = report_card.find('b').find('u').text
        print(num_report_card)
        tables = report_card.find_all(
            'table', class_='generaltable')
        for tab in tables:
            semestrs: dict[int, list] = {}
            num = 1
            semestr = 1
            for tr in tab.find('tbody').find_all('tr'):
                i = 0
                temp = {'num': num}
                lesson = tr.find_all('td')[1:]
                semestr_from_tab = int(lesson[1].text)
                for td in lesson:
                    if semestr != semestr_from_tab:
                        semestr = semestr_from_tab
                        num = 1
                        temp['num'] = num
                    temp[self.colums[i]] = td.text
                    i += 1
                num += 1
                if semestr not in semestrs:
                    semestrs[semestr] = []
                semestrs[semestr].append(temp)
            res.append(semestrs)
        print(res)

    def online_service(self):
        soup = self.get_decode_BS(self.funcs['online_service']).find(
            'div', class_='region-content')
        switcher = soup.find('form', id='switchsid')
        data = {el['name']: el['value'] for el in switcher.find_all('input')}
        sids = {el.text: el['value'] for el in switcher.find_all('option')}


