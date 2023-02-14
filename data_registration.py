import sqlite3

"""Создание базы данных"""
db = sqlite3.connect("registration.db")
print("Подключились к базе данных")
cur = db.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS users_data
    (UserID INTEGER PRIMARY KEY AUTOINCREMENT,
     Login TEXT NOT NULL,
     Password TEXT NOT NULL,
     Code INTEGER NOT NULL);
     """)
db.commit()
print("Создание таблицы users_data")

all_users = cur.execute("""SELECT * FROM users_data;""")
all_name_users = [user[1] for user in all_users]
"""Создание нулевого пациента)))"""

first_user = ('Ivan', 'qwer1234', 1234)
if first_user[0] not in all_name_users:
    cur.execute("""INSERT INTO users_data(Login, Password, Code) 
        VALUES(?, ?, ?);""", first_user)
    db.commit()
    print(f"Первый пользователь {first_user[0]} создан")


class CheckErrors:
    """Для нужд скрипта"""
    text_error = "Вы ввели не правильную операцию"
    text_error_v2 = "Логин с таким названием уже существует, либо вы ввели недопустимое значение"

    @staticmethod
    def drop_table():
        """Удаление таблицы"""
        cur.execute("""DROP TABLE users_data""")
        db.commit()
        print("Удаление таблицы")

    @staticmethod
    def counter_errors(count_cr):
        """Метод информирует об оставшихся попытках, в случае их окончания выходит из программы"""

        match count_cr:
            case 1: print("Осталось две попытки")
        match count_cr:
            case 2: print("Осталась одна попытка")
        match count_cr:
            case 3:
                print("Вы потратили все попытки, До свидания!")
                exit()


action_text = "Выбери действие: \n " \
              "Регистрация в системе - 1 \n " \
              "Авторизоваться в системе - 2 \n " \
              "Изменить пароль в системе - 3 \n"
action = input(action_text)

count = 0
while count < 3:
    try:
        validation = int(action)
        match validation:
            case 1:
                login = input("Введите логин \n")
                count = 0
                cur.execute("""SELECT Login FROM users_data;""")
                all_logins_lst = cur.fetchall()
                gen = (log[0] for log in all_logins_lst)
                while count < 4:
                    if len(login) < 2 or login.isdigit() or login in gen or not login.isascii():
                        print(CheckErrors.text_error_v2)
                        count += 1
                        CheckErrors.counter_errors(count)
                        login = input("Введите логин \n")
                    else:
                        password = input("Введите пароль \n")
                        count = 0
                        while count < 3:
                            if len(password) > 4 and password.isascii():
                                break
                            else:
                                print("Пароль не может быть меньше четырех символов и должен быть на латинице")
                                count += 1
                                CheckErrors.counter_errors(count)
                                password = input("Введите пароль \n")
                        if len(password) > 4:
                            print("Пароль установлен")
                            code = input("Введите пин-код \n")
                            count = 0
                            while count < 3:
                                if code.isdigit() and len(code) == 4:
                                    cur.execute("""INSERT INTO users_data(
                                                                Login, Password, Code)
                                                            VALUES(?, ?, ?)""", (login, password, code))
                                    db.commit()
                                    print("Добавление новых данных в таблицу")
                                    exit()
                                else:
                                    print("Пин-код должен быть из четырех чисел")
                                    count += 1
                                    CheckErrors.counter_errors(count)
                                    code = input("Введите пин-код \n")
                        break

            case 2:
                """Авторизация"""

                all_users = cur.execute("""SELECT * FROM users_data;""")
                all_password_users = [user[2] for user in all_users]
                count = 0
                login_input = input("Введите логин \n")
                while count < 3:
                    if login_input not in all_name_users:
                        print("Пользователя с таким логином нет в системе")
                        count += 1
                        CheckErrors.counter_errors(count)
                        login_input = input("Введите логин \n")
                    else:
                        cur.execute("""SELECT * FROM users_data""")
                        result = cur.fetchall()
                        password_data = 0
                        for value in result:
                            if value[1] == login_input:
                                password_data = value[2]
                        password_input = input("Введите пароль \n")
                        count = 0
                        while count < 3:
                            if password_data == password_input:
                                print("Авторизация прошла успешно")
                                exit()
                            else:
                                print("Вы ввели неправильный пароль")
                                count += 1
                                CheckErrors.counter_errors(count)
                                password_input = input("Введите пароль \n")
                        break

            case 3:
                """Изменить пароль"""
                login_update = input("Введите логин \n")
                count = 1
                while count < 3:
                    if login_update not in all_name_users:
                        print("Логин с таким именем не существует в базе")
                        count += 1
                        CheckErrors.counter_errors(count)
                        login_update = input("Введите логин \n")
                    else:
                        cur.execute("""SELECT * FROM users_data""")
                        result = cur.fetchall()
                        pin_code_data = 0
                        for value in result:
                            if value[1] == login_update:
                                pin_code_data = value[3]
                        pin_code = input("Введите пин-код \n")
                        count = 0
                        while count < 3:
                            if pin_code_data != int(pin_code):
                                print("Вы ввели неверный пин-код")
                                count += 1
                                CheckErrors.counter_errors(count)
                                pin_code = input("Введите пин-код \n")
                            else:
                                password_update = input("Введите новый пароль \n")
                                params = password_update, login_update, pin_code_data
                                cur.execute("""UPDATE users_data SET Password = ? WHERE Login = ? and Code = ?""",
                                            params)
                                db.commit()
                                print(f"Пароль изменен на {password_update}")
                                exit()
                        break
            case _:
                print("Пожалуйста введите номер операции")
                count += 1
                CheckErrors.counter_errors(count)
                action = input(action_text)

    except ValueError:
        print("Пожалуйста введите номер операции")
        count += 1
        CheckErrors.counter_errors(count)
        action = input(action_text)
