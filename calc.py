import math
from datetime import date
import json
import os
import getpass
import re
file = os.path.join('users.json')
file_history = os.path.join('history.json')

class BaseMath:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    add = (lambda a, b: a + b)
    mul = (lambda a, b: a * b)
    sub = (lambda a, b: a - b)
    div = (lambda a, b: a / b)


class SuperMath(BaseMath):
    def __init__(self, **params):
        self.userid = self
    cos = (lambda a: math.cos(a))
    sin = (lambda a: math.sin(a))
    tan = (lambda a: math.tan(a))
    ctg = (lambda a: math.cos(a) / math.sin(a))

    def history_read(userid):
        with open(file_history, 'r') as history_data:
            try:
                list_history = json.load(history_data)
                for data in list_history:
                    if data['userid'] == userid:
                        print(" id {} \n date {} \n result {} \n".format(data['id'], data['date'], data['result']))
                return ''
            except:
                print('ther is no history')
                return False

    def history(**history):
        if not os.path.isfile(file_history):
            history.update(
                {'id': 1}
            )
            user_data = []
        else:
            with open(file_history, 'r') as data:
                user_data = json.load(data)
                new_id = user_data[-1]['id'] + 1
                history.update({
                    'id': new_id
                })
        with open(file_history, 'w+') as users:
            user_data.append(history)
            json.dump(user_data, users)
        return history


def check_user_in_db(login, password=None):
    if not os.path.isfile(file):
        return False
    else:
        with open(file, 'r') as users:
            try:
                list_users = json.load(users)
                if password is None:
                    for user in list_users:
                        if user['login'] == login:
                            return True
                elif password:
                    for user in list_users:
                        if user['login'] == login:
                            if user['password'] == password:
                                return user['id']
                            else:
                                print('incorrect password\n')
            except:
                return False


def write_to_db(**new_user):
    if not os.path.isfile(file):
        new_user.update(
            {'id': 1}
        )
        user_data = []
    else:
        with open(file, 'r') as users:
            user_data = json.load(users)
            new_id = user_data[-1]['id'] + 1
            new_user.update({
                'id': new_id
            })
    with open(file, 'w+') as users:
        user_data.append(new_user)
        json.dump(user_data, users)
    return new_user


def validate_password(password, confirm_password):
    if len(password) >= 8 and password == confirm_password:
        num_of_cap = sum(1 for elem in password if elem.isupper())
        num_of_num = len(re.findall(r'[0-9]',password))
        if num_of_num >= 2 and num_of_cap >= 1:
            return True
        else:
            raise Exception('Password not valid')
    else:
        raise Exception('Password not valid')


def register(login):
    repeat_register = True
    user = None
    while repeat_register:
        try:
            password = getpass.getpass('password >>>')
            confirm_password = getpass.getpass('repeat password >>>')
            if validate_password(password, confirm_password):
                try:
                    user = write_to_db(login=login, password=password)
                    repeat_register = False
                    print('register success!')
                except ValueError as e:
                    repeat_register = True
                    print(e)
            else:
                print('incorrect password')
        except Exception as e:
            print(e, type(e))
    return user


def operations(user):
    action = ''
    while action != 'exit':
        print("Please inout operation in text mode like a + b, a - b, a * b, a / b or print 'exit' for login")
        if user:
            print('or cos a, sin a, tan a, ctg a\nprint history to view history for day')
        action = input('input your operation\n')
        for i in action.split():
            try:
                calc = {'+': SuperMath.add, '-': SuperMath.sub, '*': SuperMath.mul, '/': SuperMath.div}
                if i == '+' or i == '-' or i == '*' or i == '/':
                    res = calc[i](float(action.split()[0]), float(action.split()[2]))
                    print(res)
                    if user:
                        SuperMath.history(date=str(date.today()), result=str(action + ' = ' + str(res)), userid=user)
                if user:
                    if i == 'cos' or i == 'sin' or i == 'tan' or i == 'ctg':
                        calc = {'sin': SuperMath.sin, 'cos': SuperMath.cos, 'tan': SuperMath.tan, 'ctg': SuperMath.ctg}
                        res = calc[i](float(action.split()[1]))
                        print(res)
                        SuperMath.history(date=str(date.today()), result=str(action + ' = ' + str(res)), userid=user)
                    elif i == 'history':
                        print(SuperMath.history_read(userid=user))
            except Exception as e:
                print(e)


def main():
    while True:
        login_input = (input('please input login, leave blank for anonimus \nor print "exit" to close programm >> '))
        if login_input == 'exit':
            exit(0)
        elif len(login_input) == 0:
            operations(False)
        else:
            if check_user_in_db(login_input):
                password_input = getpass.getpass('password >>>')
                userid = check_user_in_db(login_input, password_input)
                if userid:
                    try:
                        operations(userid)
                    except Exception as e:
                        print(e, type(e))
            else:
                print('New user ', login_input, ' enter')
                register(login_input)


main()
