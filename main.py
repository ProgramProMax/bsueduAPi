import requests
from bs4 import BeautifulSoup as BS


user = input("Введите логин: ")
password = input("Введите пароль: ")

lol = {
    "username": user,
    "password": password
}
HEDERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'ru,en;q=0.9,ja;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '45',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '',
    'Host': 'dekanat.bsu.edu.ru',
    'Origin': 'https://dekanat.bsu.edu.ru',
    'Referer': 'https://dekanat.bsu.edu.ru/',
    'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36'
}
# Регистрация
session = requests.Session()
COOKIE = session.get("https://dekanat.bsu.edu.ru").cookies

# Авторизация
post1 = session.post("https://dekanat.bsu.edu.ru/login/index.php", data=lol, cookies=COOKIE, allow_redirects=False)
print(post1.status_code)
COOKIE = post1.cookies
loc = post1.headers.pop('Location')
ik = (loc.split("?")[1]).split("=")
print(ik)
# Проверка
pol = session.get(loc, data={ik[0]: ik[1]}, cookies=COOKIE)
print(pol.status_code)
UUID = ik[1]

mop = session.get("https://dekanat.bsu.edu.ru/", cookies=COOKIE)
print(mop.status_code)
res = str(mop.content.decode('utf-8'))

session.get("https://dekanat.bsu.edu.ru/blocks/bsu_other/new_journal/index.php?uid=153766",data={f"uid={UUID}":UUID}, cookies=COOKIE)
print(BS(res, "lxml").find("div", class_="logininfo").text)
