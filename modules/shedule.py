import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime, timedelta
import re


class shedule:

    def __init__(self, num_group) -> None:
        self.num_group = num_group

    def get_lesson(self, startdate):
        start_date: datetime = datetime.strptime(startdate, '%d.%m.%Y')
        end_date = start_date + timedelta(days=6)
        post = {
            "group": self.num_of_group,
            "week": start_date.strftime('%d%m%Y')+end_date.strftime('%d%m%Y')
        }
        html = requests.post(
          "https://bsuedu.ru/bsu/education/schedule/groups/show_schedule.php",
          data=post)
        soup = BS(str(html.content.decode("utf-8")), "lxml")
        lessons = {}
        trs = soup.find("table", id='shedule').find_all("tr")
        day = ''
        num = 0
        time = ''
        for tr in trs:
            if isinstance(tr.find('td', class_='colspan'), None):
                day = tr.find('td', class_='colspan').text.replace(
                    '\n',
                    '').replace(' (сегодня)', '')
                print(day)
                lessons[day] = []
            else:
                lesson = {}
                for col in tr.find_all('td'):
                    match col['id']:
                        case 'num':
                            lesson['num'] = col.text.replace(
                                '\n', '').replace(' пара', '')
                            num = lesson['num']
                        case 'time':
                            lesson['time'] = col.text.replace(
                                '\n', '').replace(' ', '')
                            time = lesson['time']
                        case 'lesson':
                            if col['width'] == '1%':
                                lesson['type_lesson'] = col.text.replace('\n', '')
                            elif col['width'] == '33%':
                                pop = col.text.replace('\n', '').replace(
                                    '  ', '').split(') ')
                                if len(pop) == 2:
                                    lesson['num'] = num
                                    lesson['time'] = time
                                    lesson['under_group'] = pop[0]+')'
                                    lesson['lesson'] = pop[1].split(' (')[0]
                                else:
                                    lesson['lesson'] = pop[0]
                                hrefs = col.find_all('a')
                                if len(hrefs) == 1:
                                    lesson['href'] = {'В курс', hrefs[0]['href']}
                                else:
                                    lolipop = {}
                                    for href in hrefs:
                                        lolipop[href.text.replace('\n', '')] = href['href']
                                    lesson['href'] = lolipop
                        case 'teacher':
                            tech = col.text.replace('\n', '')
                            if tech == ' ':
                                lesson['teacher'] = None
                            else:
                                lesson['teacher'] = tech
                        case 'aud':
                            corp = col.text.replace('\n', '').replace(
                                '  ', '').split(',У')
                            if len(corp) == 2:
                                lesson['aud'] = corp[0].replace('ауд. ', '')
                                if corp[1].find('онлайн') != -1:
                                    lesson['corp'] = re.match(
                                        r'\d{1,2}',
                                        corp[1][corp[1].find('№')+1:]).group(0)
                                    lesson['online'] = True
                                else:
                                    lesson['corp'] = re.match(
                                        r'\d{1,2}',
                                        corp[1][corp[1].find('№')+1:]).group(0)
                                    lesson['online'] = False
                            else:
                                lesson['corp'] = None
                                lesson['online'] = True
                lessons[day].append(lesson)
        return lessons
