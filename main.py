import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if # Можно и так, но лаконичнее просто dt.datetime.today()
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        # Давай добавим к каждому методу Docstrings.
        # Почитать что это такое можно здесь: https://peps.python.org/pep-0257/#what-is-a-docstring
        # Если пользоваться ими и правильно оформлять, твой код станет выглядеть солиднее
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:     # Используем имя класса "Record". Разберемся, как правильно пройтись по листу? (P.S. методом ниже правильно)
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0 # Давай используем "chained comparison", что дословное - цепное сравнение.
                                                # https://www.geeksforgeeks.org/chaining-comparison-operators-python/
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \   # Здесь f-строка нам не нужна. Только строкой ниже
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:  # P.S. В данном случае здесь else излишен. Если сработало условие выше, то до else дело не дойдет - выйдет с return
            return  ('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE): # По условию, мы вызываем данный метод
                                                                        # только с переменной "currency".
                                                                        # Поэтому изменение значений валют здесь излишний

        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd': # Может подумаем над другой записью проверки валют? Что если у нас будет 50 валют?
                              # Придется проверять каждую через if-elif, что не очень хорошо. P.S. мы всегда знаем,
                              # в каком виде придет валюта
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00  # Небольшая ошибка)
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} ' #  У f-строк есть крутая фишка - изменение формата. 
                                                                # Можно отформатировать сточку прямо внутри f-строки.
                                                                # Например здесь: f'На сегодня осталось {cash_remained:.2f}
                f'{currency_type}'
            )
        elif cash_remained == 0: # Смотри, столько кода выше, а у нас тут денег нет. Оказывается код выше
                                # не пригодился, повод рассмотреть правильный порядок действий
            return 'Денег нет, держись'
        elif cash_remained < 0: # Лучше использовать else, раз это последний случай.
                                # Но так же можно обойтись и без else,
                                # так же как и в случае с else выше
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type) # Чтобы привести вывод строк к одному формату,
                                                                    # можно так же вывести код, как мы сделали в первом if

    def get_week_stats(self):
        super().get_week_stats()    # Раз мы в этой функции ничего не меняем, то можно удалить
                                    # этот метод. Он и так вызовет родительский метод


# В коде есть несколько ошибок(синтаксические, несоответствие ТЗ)
# Внутри задания есть примеры тестов, для проверки работоспособности кода. Давай их добавим сюда
# И можно добавить еще свои тесты. Тогда мы точно узнаем, что наш код работает правильно.