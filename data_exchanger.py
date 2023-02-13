import sqlite3

from selenium import webdriver
from selenium.webdriver.common.by import By

"""

Тестовое задание: "Обмен валюты" с применением Объектно-Ориентированного Программирования и SQL
сделано на одной странице специально, такое условие задания.  

"""

"""Считываем актуальные значения курса валют с сайта 'banki.ru'"""
driver = webdriver.Firefox(executable_path='D:\\selenium_pr\\geckodriver.exe.exe')
driver.get('https://www.banki.ru/products/currency/cb/')
driver.get('https://www.banki.ru/products/currency/cb/')
usd_locator = driver.find_element(By.XPATH,
                                  '/html/body/div[1]/div[1]/main/div[2]/table/tbody/tr[1]/td[4]')
eur_locator = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/main/div[2]/table/tbody/tr[2]/td[4]')

usd = float(usd_locator.text)
eur = float(eur_locator.text)
driver.close()

"""Создание базы данных"""
db = sqlite3.connect("exchanger.db")
print("Connect to data-base")
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users_balance(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Balance_RUB INTEGER NOT NULL,
            Balance_USD INTEGER NOT NULL,
            Balance_EUR INTEGER NOT NULL);
            """)
db.commit()


class Requests_DB:
    """Класс с запросами к базе данных"""

    @staticmethod
    def select_all_users():
        """Get all accounts info"""
        all_balance = cur.execute("""SELECT * FROM users_balance;""")
        return all_balance

    @staticmethod
    def select_all_users_with_params():
        """Get all currency account info"""
        Requests_DB.select_all_users()
        value = cur.fetchall()
        rub = value[0][1]
        usd = value[0][2]
        eur = value[0][3]
        return [round(rub, 2), round(usd, 2), round(eur, 2)]


all_id_users = [user[0] for user in Requests_DB.select_all_users()]
first_user_balance = (1, 100000, 1000, 1000)

"""Create first_user account"""

if first_user_balance[0] not in all_id_users:
    cur.execute("""INSERT INTO users_balance
        (UserID, Balance_RUB, Balance_USD, Balance_EUR)
        VALUES(?, ?, ?, ?)""", first_user_balance)
    db.commit()


class Users_Balance:
    """Get balance users info"""

    def __init__(self, balance_rub, balance_usd, balance_eur):
        self.balance_rub = balance_rub
        self.balance_usd = balance_usd
        self.balance_eur = balance_eur

    def get_balance_rub(self):
        """get rub account info"""
        print(f"На вашем балансе: {self.balance_rub} RUB")

    def get_balance_usd(self):
        """get usd account info"""
        print(f"На вашем балансе: {self.balance_usd} USD")

    def get_balance_eur(self):
        """get eur account info"""
        print(f"На вашем балансе: {self.balance_eur} EUR")


class Currency:
    """Change currency class"""

    def __init__(self, rub, usd, eur):
        self.rub = rub
        self.usd = usd
        self.eur = eur

    def change_usd_eur(self, value):
        """pair usd - eur"""
        print("Валютная пара usd - eur")
        return round((self.usd / self.eur) * value, 2)

    def change_eur_usd(self, value):
        """pair eur - usd"""
        print("Валютная пара eur - usd")
        return round((self.eur / self.usd) * value, 2)

    def change_rub_usd(self, value):
        """pair rub - usd"""
        print("Валютная пара rub - usd")
        return round(value / self.usd, 2)

    def change_usd_rub(self, value):
        """pair usd - rub"""
        print("Валютная пара usd - rub")
        return round(value * self.usd, 2)

    def change_rub_eur(self, value):
        """pair rub - eur"""
        print("Валютная пара rub - eur")
        return round(value / self.eur, 2)

    def change_eur_rub(self, value):
        """pair eur - rub """
        print("Валютная пара eur - rub")
        return round(value * self.eur, 2)


class Check_Input_Value:
    """Методы для проверки валидации"""

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


"""Актуальный курс валюты"""
rate = Currency(1, usd, eur)

"""Приветствие"""

print(
    f"Добро пожаловать в наш обменный пункт, курс валют следующий: "
    f"\n USD = {round(rate.usd, 2)} RUB"
    f"\n EUR = {round(rate.eur, 2)} RUB"
    f"\n USD = {round(rate.usd / rate.eur, 2)} EUR"
    f"\n EUR = {round(rate.eur / rate.usd, 2)} USD")

"""Выбор валюты"""
choice_currency = 0  # для использования глобальной переменной


def select_currency():
    """Метод выбора валюты"""
    text_for_choice_currency = "Введите какую валюту желаете обменять: \n 1. RUB \n 2. USD \n 3. EUR \n"
    count = 0
    global choice_currency
    choice_currency = input(text_for_choice_currency)
    while count < 3:
        if choice_currency.isdigit() and 0 < int(choice_currency) < 4:
            break
        else:
            count += 1
            Check_Input_Value.counter_errors(count)
            choice_currency = input(text_for_choice_currency)


"""Выбор суммы"""
input_sum = 0


def select_sum():
    """Метод выбора суммы"""
    text_for_input_sum = "Какая сумма Вас интересует? \n"
    text_sum_error = "На вашем счету недостаточно средств, введите сумму меньше"
    count = 0
    while count < 3:
        try:
            global input_sum
            input_sum = int(input(text_for_input_sum))
            count = 0
        except ValueError:
            count += 1
            Check_Input_Value.counter_errors(count)
        else:
            param = Requests_DB.select_all_users_with_params()
            if input_sum <= param[int(choice_currency) - 1]:
                break
            else:
                print(text_sum_error)
                count += 1
                Check_Input_Value.counter_errors(count)


"""Выбор валюты на обмен"""
choice_currency_for_change = 0


def select_currency_for_change(second_value):
    """Метод выбора валюты на обмен"""

    text_for_choice_currency_for_change = "Какую валюту готовы предложить взамен \n 1. RUB \n 2. USD \n 3. EUR \n"
    text_error_choice = "введите другую валюту"
    count = 0
    while count < 3:
        try:
            global choice_currency_for_change
            choice_currency_for_change = int(input(text_for_choice_currency_for_change))
            count = 0
        except ValueError:
            count += 1
            Check_Input_Value.counter_errors(count)
        else:
            if choice_currency_for_change != second_value and 0 < choice_currency_for_change < 4:
                break
            else:
                print(text_error_choice)
                Check_Input_Value.counter_errors(count)
                count += 1
                choice_currency_for_change = input(text_for_choice_currency_for_change)


def select_currency_pair(currency_1, currency_2):
    """Выбор валютной пары для обмена"""

    params = Requests_DB.select_all_users_with_params()  # Запрос в базу данных

    # pair rub - usd

    if int(currency_1) == 1 and int(currency_2) == 2:
        data_user_rub = (float(params[0]) - float(input_sum)), 1
        cur.execute("""UPDATE users_balance SET Balance_RUB = ? WHERE UserID = ?""", data_user_rub)
        data_user_usd = (float(rate.change_rub_usd(float(input_sum)) + float(params[1])), 1)
        cur.execute("""UPDATE users_balance SET Balance_USD = ? WHERE UserID = ?""", data_user_usd)
        db.commit()
        print("Операция прошла успешно")
        params = Requests_DB.select_all_users_with_params()
        user = Users_Balance(params[0], params[1], params[2])
        Users_Balance.get_balance_rub(user)
        Users_Balance.get_balance_usd(user)

    # pair rub - eur

    elif int(currency_1) == 1 and int(currency_2) == 3:
        data_user_rub = (float(params[0]) - float(input_sum)), 1
        cur.execute("""UPDATE users_balance SET Balance_RUB = ? WHERE UserID = ?""", data_user_rub)
        data_user_eur = (float(rate.change_rub_eur(float(input_sum)) + float(params[2])), 1)
        cur.execute("""UPDATE users_balance SET Balance_EUR = ? WHERE UserID = ?""", data_user_eur)
        db.commit()
        print("Операция прошла успешно")
        params = Requests_DB.select_all_users_with_params()
        user = Users_Balance(params[0], params[1], params[2])
        Users_Balance.get_balance_rub(user)
        Users_Balance.get_balance_eur(user)

    # pair usd - rub

    elif int(currency_1) == 2 and int(currency_2) == 1:
        data_user_usd = (float(params[1]) - float(input_sum)), 1
        cur.execute("""UPDATE users_balance SET Balance_USD = ? WHERE UserID = ?""", data_user_usd)
        data_user_rub = (float(rate.change_usd_rub(float(input_sum)) + float(params[0])), 1)
        cur.execute("""UPDATE users_balance SET Balance_RUB = ? WHERE UserID = ?""", data_user_rub)
        db.commit()
        print("Операция прошла успешно")
        params = Requests_DB.select_all_users_with_params()
        user = Users_Balance(params[0], params[1], params[2])
        Users_Balance.get_balance_usd(user)
        Users_Balance.get_balance_rub(user)

    # pair usd - eur

    elif int(currency_1) == 2 and int(currency_2) == 3:
        data_user_usd = (float(params[1]) - float(input_sum)), 1
        cur.execute("""UPDATE users_balance SET Balance_USD = ? WHERE UserID = ?""", data_user_usd)
        data_user_eur = (float(rate.change_usd_eur(float(input_sum)) + float(params[2])), 1)
        cur.execute("""UPDATE users_balance SET Balance_EUR = ? WHERE UserID = ?""", data_user_eur)
        db.commit()
        print("Операция прошла успешно")
        params = Requests_DB.select_all_users_with_params()
        user = Users_Balance(params[0], params[1], params[2])
        Users_Balance.get_balance_usd(user)
        Users_Balance.get_balance_eur(user)

    # pair eur - rub

    elif int(currency_1) == 3 and int(currency_2) == 1:
        data_user_eur = (float(params[2]) - float(input_sum)), 1
        cur.execute("""UPDATE users_balance SET Balance_EUR = ? WHERE UserID = ?""", data_user_eur)
        data_user_rub = (float(rate.change_eur_rub(float(input_sum)) + float(params[0])), 1)
        cur.execute("""UPDATE users_balance SET Balance_RUB = ? WHERE UserID = ?""", data_user_rub)
        db.commit()
        print("Операция прошла успешно")
        params = Requests_DB.select_all_users_with_params()
        user = Users_Balance(params[0], params[1], params[2])
        Users_Balance.get_balance_eur(user)
        Users_Balance.get_balance_rub(user)

    # pair eur - usd

    elif int(currency_1) == 3 and int(currency_2) == 2:
        data_user_eur = (float(params[2]) - float(input_sum)), 1
        cur.execute("""UPDATE users_balance SET Balance_EUR = ? WHERE UserID = ?""", data_user_eur)
        data_user_usd = (float(rate.change_eur_usd(float(input_sum)) + float(params[1])), 1)
        cur.execute("""UPDATE users_balance SET Balance_USD = ? WHERE UserID = ?""", data_user_usd)
        db.commit()
        print("Операция прошла успешно")
        params = Requests_DB.select_all_users_with_params()
        user = Users_Balance(params[0], params[1], params[2])
        Users_Balance.get_balance_eur(user)
        Users_Balance.get_balance_usd(user)


def drop_table():
    """Удаление таблицы"""
    cur.execute("""DROP TABLE users_balance""")
    db.commit()
    print("Удаление таблицы")


def start_program():
    select_currency()
    select_sum()
    select_currency_for_change(choice_currency)
    select_currency_pair(choice_currency, choice_currency_for_change)


start_program()
