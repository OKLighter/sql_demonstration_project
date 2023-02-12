import sqlite3

"""Программа "Обмен валюты" с применением Объектно-Ориентированного Программирования и SQL"""

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
        return round(value / self.eur, 2)

    def change_eur_usd(self, value):
        """pair eur - usd"""
        print("Валютная пара eur - usd")
        return round(value / self.usd, 2)

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
    def check_input(first_value, second_value, text_error, text_input):
        """Метод для проверки значений на равно с тремя попытками"""

        count = 0
        while count < 4:
            if first_value == second_value:
                print(text_error)
                count += 1
                if count == 2:
                    print(f"Осталась последняя попытка")
                if count == 3:
                    print("Вы потратили все попытки, До свидания!")
                    break
                second_value = input(text_input)
            else:
                break

    @staticmethod
    def check_sum_in_balance(sum_input, sum_balance, text_error, text_input):
        """Метод для проверки на больше с тремя попытками"""
        count = 0
        while count < 4:
            if float(sum_input) > float(sum_input):
                print(sum_input)
                print(sum_balance)
                print(text_error)
                count += 1
                if count == 2:
                    print(f"Осталась последняя попытка")
                if count == 3:
                    print("Вы потратили все попытки, До свидания!")
                    break
                sum_input = input(text_input)
            else:
                break


"""Актуальный курс валюты"""
rate = Currency(1, 70, 80)

"""Приветствие"""

print(
    f"Добро пожаловать в наш обменный пункт, курс валют следующий: "
    f"\n USD = {rate.usd} RUB"
    f"\n EUR = {rate.eur} RUB"
    f"\n USD = {round(rate.usd / rate.eur, 2)} EUR"
    f"\n EUR = {round(rate.eur / rate.usd, 2)} USD")

"""Выбор валюты"""
choice_currency = 0  # для использования глобальной переменной


def select_currency():
    text_for_choice_currency = "Введите какую валюту желаете обменять: \n 1. RUB \n 2. USD \n 3. EUR \n"
    count = 0
    global choice_currency
    choice_currency = input(text_for_choice_currency)
    while count < 7:
        if choice_currency.isdigit() and 0 < int(choice_currency) < 4:
            break
        else:
            count += 1
            if count == 5:
                print("Осталось две попытки")
            if count == 6:
                print(f"Осталась одна попытка")
            if count == 7:
                print("Вы потратили все попытки, До свидания!")
                exit()
            choice_currency = (input(text_for_choice_currency))


"""Выбор суммы"""
input_sum = 0


def select_sum():
    text_for_input_sum = "Какая сумма Вас интересует? \n"
    text_sum_error = "На вашем счету недостаточно средств, введите сумму меньше"
    count = 0
    while count < 7:
        try:
            global input_sum
            input_sum = int(input(text_for_input_sum))
        except ValueError:
            if count == 4:
                print(f"Осталось две попытки")
            if count == 5:
                print(f"Осталась одна попытка")
            if count == 6:
                print("Вы потратили все попытки, До свидания!")
                exit()
            count += 1
        else:
            param = Requests_DB.select_all_users_with_params()
            if input_sum < param[int(choice_currency) - 1]:
                break
            else:
                print(text_sum_error)
                if count == 4:
                    print(f"Осталось две попытки")
                if count == 5:
                    print(f"Осталась одна попытка")
                if count == 6:
                    print("Вы потратили все попытки, До свидания!")
                    exit()
                count += 1


select_currency()
select_sum()

"""Выбор валюты для обмена"""

text_for_choice_currency_for_change = "Какую валюту готовы предложить взамен \n 1. RUB \n 2. USD \n 3. EUR \n"
text_error_choice = "Невозможно произвести обмен двух одинаковых валют, введите другую валюту"
choice_currency_for_change = input(text_for_choice_currency_for_change)
Check_Input_Value.check_input(choice_currency, choice_currency_for_change, text_error_choice,
                              text_for_choice_currency_for_change)

params = Requests_DB.select_all_users_with_params()

# pair rub - usd

if int(choice_currency) == 1 and int(choice_currency_for_change) == 2:
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

elif int(choice_currency) == 1 and int(choice_currency_for_change) == 3:
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

elif int(choice_currency) == 2 and int(choice_currency_for_change) == 1:
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

elif int(choice_currency) == 2 and int(choice_currency_for_change) == 3:
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

elif int(choice_currency) == 3 and int(choice_currency_for_change) == 1:
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

elif int(choice_currency) == 3 and int(choice_currency_for_change) == 2:
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

# """Удаление таблицы"""
# cur.execute("""DROP TABLE users_balance""")
# db.commit()
# print("Удаление таблицы")
