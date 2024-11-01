from modules.bsuAPI import BSU

active_users: dict[int, BSU] = {}

if __name__ == '__main__':
    print('Запуск')
    id = 10
    print('Авторизация')
    student = BSU(username="1387339", password="1024815886749Try+", dekanat_on=True)
    if student.is_auth:
        dekanat = student._dekanat
        print('Авторизован')
        dekanat.get_function()
        dekanat.get_report_card()
