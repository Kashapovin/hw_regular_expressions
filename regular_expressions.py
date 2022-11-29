import csv
import re

data = []
with open('phonebook_raw.csv', encoding='utf-8') as file:
    fields = file.readline().strip().split(',')
    reader = csv.DictReader(file, fieldnames=fields)
    for row in reader:
        pattern = '([А-Яа-я]+)\s?([А-Яа-я]+)?\s{0,1}([А-Яа-я]+)?'

        res = re.search(pattern, row['lastname'])

        lastname, firstname, surname = res.group(1), res.group(2), res.group(3)

        pattern2 = '([А-Яа-я]+)?\s?([А-Яа-я]+)?'
        res = re.search(pattern2, row['firstname'])
        firstname2, surname2 = res.group(1), res.group(2)

        row['lastname'] = lastname
        firstname = firstname or firstname2
        row['firstname'] = firstname
        surname = surname or surname2 or row['surname']
        row['surname'] = surname

        phone_pattern = r'(\+7|8)?\s?\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})\s?\(?(доб.\s\d{4})?\)?'
        if row['phone']:
            res = re.sub(phone_pattern, r'+7(\2)\3-\4-\5 \6', row['phone'])
            row['phone'] = res
        row = {key: value for key, value in row.items() if key is not None}
        data.append(row)

data = sorted(data, key=lambda i: i['lastname'])
data1 = data.copy()

for i in range(1, len(data)):
    if data[i-1]['lastname'] == data[i]['lastname']:
        for key, value in data[i].items():
            data[i][key] = value if value else data[i-1][key]
        data1.remove(data[i-1])

print(data1)

with open('phonebook.csv', 'w', encoding='utf-8', newline='') as file:
    datawriter = csv.DictWriter(file, fieldnames=fields)
    datawriter.writeheader()
    datawriter.writerows(data1)
