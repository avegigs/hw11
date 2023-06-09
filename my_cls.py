from collections import UserDict
from datetime import datetime
import re


class AddressBook(UserDict):
    def add_record(self, record):
        key = record.name.value
        self.data[key] = record
        # print(f'key is {key}')

    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {str(record)}'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''

    # def search(self, search_string):
    #     search_result = []
    #     for record in self.data.values():
    #         if search_string in record.name.value:
    #             search_result.append(record)
    #         else:
    #             for phone in record.phones:
    #                 if search_string in phone.value:
    #                     search_result.append(record)
    #                     break
    #     return search_result


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


class Name(Field):

    def __init__(self, value):
        self.value = value
    # def __init__(self, name):
    #     self.value = name
    #     self.name = name

    # def __str__(self) -> str:
    #     return self.name

    # def __repr__(self) -> str:
    #     return self.name


class Phone(Field):

    def __init__(self, value):
        self.value = value

    @Field.value.setter
    def value(self, value):
        if not re.match(r'^\+38\d{10}$', value):
            raise ValueError(
                "Phone number should be in the format +380XXXXXXXXX")
        Field.value.fset(self, value)

    def __str__(self) -> str:
        return self.__value

    def __repr__(self) -> str:
        return self.value

        # @Private.value.setter
    # def value(self, value):
    #     if not isinstance(value, int):
    #         raise Exception(f"'{value}' is not a valid")
    #     Private.value.fset(self, value)


class Birthday(Field):

    @Field.value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            raise Exception("Invalid birthday. Only string format dd.mm.yyyy")
        Field.value.fset(self, value)

    def __str__(self) -> str:
        return datetime.strftime(self.__value, '%d.%m.%Y')

    def __repr__(self) -> str:
        return datetime.strftime(self.__value, '%d.%m.%Y')


class Record:
    def __init__(self, name: Name, birthday: Birthday = None):
        self.birthday = birthday
        self.name = name

        self.phones = []

    def __str__(self) -> str:
        return f'User {self.name} have phone nymbers: {self.phones}'

    def __repr__(self) -> str:
        return f'{self.phones}'

    def add_phone(self, phone: Phone):
        self.phones.append(phone.value)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    # def get_name(self):
    #     return self.name.value

    def get_phone(self, old_phone):
        for phone in self.phones:
            if phone == old_phone:
                return phone
            else:
                return None

    def days_to_birthday(self):
        if not self.birthday:
            return None
        now = datetime.now().date()
        birth = datetime.strptime(str(self.birthday), '%d.%m.%Y').date()
        if (birth.replace(year=now.year) - now).days > 0:
            return (birth.replace(year=now.year) - now).days
        return (birth.replace(year=now.year + 1) - now).days


# phone1 = Phone('+380681537636')
# birthday1 = Birthday('27.05.1988')


# phone4 = Phone('+380678889966')

# name1 = Name('Angle')
# record1 = Record(name1, birthday1)
# record1.add_phone(phone1)
# record1.add_phone(phone4)

# print(record1.days_to_birthday())

# address = AddressBook()
# address.add_record(record1)

# print(phone1.value)
# print(birthday1.value)
# print(record1)
# print(address)
