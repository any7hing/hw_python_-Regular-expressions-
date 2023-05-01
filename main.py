import re
import csv
with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

result_list, phone, name, organisation, position, email, = [], [], [], [], [], []
buff = ""
result_dict = {}


def make_contacts_list():
    for i in range(1, len(contacts_list)):
        res = (re.findall(r'\d+\s*', ''.join(contacts_list[i])))
        phone.append((''.join(res)).replace(' ', ""))
        buff = ""
        for j in range(3):
            if len(contacts_list[i][j]) > 1:
                buff += " " + contacts_list[i][j]
        name.append((buff))
        organisation.append(contacts_list[i][3])
        position.append(contacts_list[i][4])
        email.append(contacts_list[i][6])


def make_phone_number():
    for i in range(len(phone)):
        if phone[i]:
            phone[i] = '+7'+'('+phone[i][1:4]+')' + phone[i][3:]
        if len(phone[i]) > 15:
            phone[i] = phone[i][0:15] + ' доб.' + phone[i][15:]


def final_sort_list():
    for i in range(len(result_list)):
        try:
            if len((result_dict[" ".join(result_list[i][0].split()[0:2])].get('surname'))) == 0:
                result_dict[" ".join(result_list[i][0].split()[0:2])].update({'surname': " ".join(result_list[i][0].split()[2:3])})
            if len((result_dict[" ".join(result_list[i][0].split()[0:2])].get('position'))) == 0:
                result_dict[" ".join(result_list[i][0].split()[0:2])].update({'position': result_list[i][2]})
            if len((result_dict[" ".join(result_list[i][0].split()[0:2])].get('email'))) == 0:
                result_dict[" ".join(result_list[i][0].split()[0:2])].update({'email': result_list[i][4]})
            if len((result_dict[" ".join(result_list[i][0].split()[0:2])].get('phone'))) == 0:
                result_dict[" ".join(result_list[i][0].split()[0:2])].update({'phone': result_list[i][3]})
            if len((result_dict[" ".join(result_list[i][0].split()[0:2])].get('organization'))) == 0:
                result_dict[" ".join(result_list[i][0].split()[0:2])].update({'organization': result_list[i][1]})

        except (KeyError):
            result_dict[" ".join(result_list[i][0].split()[0:2])] = {}
            result_dict[" ".join(result_list[i][0].split()[0:2])] = {
                    'last_name': " ".join(result_list[i][0].split()[0:1]),
                    'first_name': " ".join(result_list[i][0].split()[1:2]),
                    'surname': " ".join(result_list[i][0].split()[2:3]),
                    'organization': result_list[i][1],
                    'position': result_list[i][2],
                    'phone': result_list[i][3],
                    'email': result_list[i][4]
                }


if __name__ == '__main__':
    make_contacts_list()
    make_phone_number()
    result_list = list(zip(name, organisation, position, phone, email))
    final_sort_list()


field_names = ['full_name', 'last_name', 'first_name', 'surname', 'organization', 'position', 'phone', 'email']
with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.DictWriter(f,delimiter=",", fieldnames=field_names, dialect='unix')
    datawriter.writeheader()
    for i in result_dict.items():
        i[1].update({'full_name':i[0]})
        datawriter.writerow(i[1])
