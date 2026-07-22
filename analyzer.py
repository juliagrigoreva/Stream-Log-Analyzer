from itertools import filterfalse
import json
from datetime import datetime
from collections import Counter

with open('file_log_server.json', 'r', encoding='utf-8') as file:
    # 1. Построчно десериализуем в генераторе
    rows = (json.loads(row.strip()) for row in file)

    # 2. Оставляем только ERROR
    sts_err = filterfalse(lambda row: row['level'] != 'ERROR', rows)

    # 3. Оставляем только ночные ошибки (до 04:00 включительно)
    night_time = (row for row in sts_err if datetime.strptime(row['timestamp'], '%Y-%m-%dT%H:%M:%S').hour <= 4)

    # Превращаем генератор в список, так как дальше нам нужно работать с индексами и запускать цикл
    for_data = list(night_time)

# Проверяем, нашли ли мы вообще хоть одну ошибку, чтобы программа не упала
if for_data:
    # Берем самый первый элемент (индекс 0) для определения даты отчета
    d = datetime.strptime(for_data[0]['timestamp'], '%Y-%m-%dT%H:%M:%S')
    reporting_date = d.strftime('%d.%m.%Y')

    # Считаем количество ошибок (исправили имя переменной в цикле на 'row')
    msg = Counter(row['msg'] for row in for_data)

    print('___________________________________________')
    print(f'Отчетные данные за период {reporting_date} с 00:00 до 04:00')
    print('___________________________________________')
    for key, value in msg.items():
        print(f'Ошибка "{key}" повторилась {value} раз(а)')
else:
    print('___________________________________________')
    print('За указанный период (00:00 - 04:00) ошибок не обнаружено.')
    print('___________________________________________')