import sqlite3


class db_connector:

    def _init__(self, name_db):
        self.__connection: sqlite3.Connection = sqlite3.connect(name_db)

    def get_colums_names(self, name_table: str) -> list:
        cur = self.__connection.cursor()
        lol = cur.execute(f"select * from {name_table}")
        sel = list(map(lambda x: x[0], lol.description))
        return sel

    # Колличесво строк

    def count(self, name_table: str, col: str = '', where: dict = {}) -> int:
        cur = self.__connection.cursor()
        wer = ""
        for key, val in where.items():
            if key == list(where.keys())[-1]:
                if type(val) is str:
                    wer += f'{key}="{val}"'
                elif type(val) is int:
                    wer += f'{key}={val}'
            else:
                if type(val) is str:
                    wer += f'{key}="{val}" and '
                elif type(val) is int:
                    wer += f'{key}={val} and '
        if wer == '':
            sel = list(cur.execute(f"SELECT COUNT({col}) FROM {name_table}").fetchone())[0]
        else:
            sel = list(cur.execute(f"SELECT COUNT({col}) FROM {name_table} WHERE {wer}").fetchone())[0]
        return sel

    # Получение данных из таблицы

    def select(self, table: str, colums: list, where: dict = {}, return_array=False, unzip=False) -> list | dict | int | str:
        cur = self.__connection.cursor()
        if colums[0] == '*':
            colums = self.get_colums_names(table)
        res = []
        wer = ''
        if where == {}:
            for row in cur.execute(f"SELECT {','.join(colums)} FROM {table}").fetchall():
                string = {}
                for i in range(0, len(colums)):
                    string[colums[i]] = row[i]
                res.append(string)
        else:
            try:
                for key, val in where.items():
                    if key == list(where.keys())[-1]:
                        if type(val) is str:
                            wer += f"{key}='{val}'"
                        elif type(val) is int:
                            wer += f"{key}={val}"
                    else:
                        if type(val) is str:
                            wer += f"{key}='{val}' and "
                        elif type(val) is int:
                            wer += f"{key}={val} and "
            except Exception:
                print("Не полное условие отбора")
            for row in cur.execute(f"SELECT {','.join(colums)} FROM {table} WHERE {wer}").fetchall():
                string = {}
                for i in range(len(colums)):
                    string[colums[i]] = row[i]
                res.append(string)
        if len(res) == 0:
            return []
        elif len(res) == 1:
            if return_array and len(colums) == 1:
                pop = []
                for row in res:
                    for key, val in row.items():
                        pop.append(val)
                return pop
            elif return_array:
                return res
            elif unzip and len(colums) == 1:
                return (res[0])[colums[0]]
            else:
                return res[0]
        else:
            if return_array and len(colums) == 1:
                pop = []
                for row in res:
                    for key, val in row.items():
                        pop.append(val)
                return pop
            if unzip and return_array:
                temp = []
                for row in res:
                    for key, val in row.items():
                        temp.append(val)
                return temp
            else:
                return res

    # Обновление

    def update(self, dict_data: dict, name_table, where: dict):
        cur = self.__connection.cursor()
        set = ""
        for key, val in dict_data.items():
            if key == list(dict_data.keys())[-1]:
                if isinstance(val, str):
                    set += f"{key}='{val}'"
                elif isinstance(val, int):
                    set += f"{key}={val}"
            else:
                if isinstance(val, str):
                    set += f"{key}='{val}', "
                elif isinstance(val, str):
                    set += f"{key}={val}, "
        wer = ""
        for key, val in where.items():
            if key == list(where.keys())[-1]:
                if isinstance(val, str):
                    wer += f"{key}='{val}'"
                elif isinstance(val, int):
                    wer += f"{key}={val}"
            else:
                if isinstance(val, str):
                    wer += f"{key}='{val}' and "
                elif isinstance(val, int):
                    wer += f"{key}={val} and "
        cur.execute(f"UPDATE {name_table} SET {set} WHERE {wer}")
        self.__connection.commit()

    # Добавление в таблицу

    def insert(self, name_table: str, data: dict) -> None:
        cur = self.__connection.cursor()
        colums = ""
        values = ""
        for key, val in data.items():
            if key == list(data.keys())[-1]:
                colums += f"{key}"
            else:
                colums += f"{key},"
            if val == list(data.values())[-1]:
                if isinstance(val, str):
                    values += f"'{val}'"
                elif isinstance(val, int):
                    values += f"{val}"
            else:
                if isinstance(val, str):
                    values += f"'{val}',"
                elif isinstance(val, int):
                    values += f"{val},"
        print(colums)
        print(values)
        cur.execute(f"INSERT INTO {name_table} ({colums}) VALUES ({values})")
        print(f"В таблицу {name_table} добавляют данные")
        self.__connection.commit()

    # Удаление из таблицы

    def delete(self, name_table: str, where: dict = {}) -> None:
        cur = self.__connection.cursor()
        wer = ""
        for key, val in where.items():
            if key == list(where.keys())[-1]:
                if isinstance(val, str):
                    wer += f"{key}='{val}'"
                elif isinstance(val, int):
                    wer += f"{key}={val}"
            else:
                if isinstance(val, str):
                    wer += f"{key}='{val}' and "
                elif isinstance(val, int):
                    wer += f"{key}={val} and "
        cur.execute(f"DELETE FROM {name_table} WHERE {wer}")
        self.__connection.commit()

    def get_stucture_of_table(self):
        cur = self.__connection.cursor()
        lol = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return lol.fetchall()
