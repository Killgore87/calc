import math
from datetime import date
import json
import os
import getpass
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


def check_user_auth(login, password):
    if not os.path.isfile(file):
        return False
    with open(file, 'r') as users:
        try:
            list_users = json.load(users)
            for user in list_users:
                if user['login'] == login and user['password'] == password:
                    return user['id']
        except:
            print('incorrect password')
            return False


def check_user_in_db(login):
    if not os.path.isfile(file):
        return False
    else:
        with open(file, 'r') as users:
            try:
                list_users = json.load(users)
                for user in list_users:
                    if user['login'] == login:
                        return True
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
        num_of_cap = 0
        num_of_num = 0
        for i in password:
            if 'A' <= i <= 'Z':
                num_of_cap += 1
            if '0' <= i <= '9':
                num_of_num += 1
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
            print('or cos a, sin a, tan a, ctg a')
            print('print history to view history for day')
        action = input('input your operation\n')
        day = date.today()

        def result_(a):
            calc = {'+': BaseMath.add, '-': BaseMath.sub, '*': BaseMath.mul, '/': BaseMath.div}
            if a == 'cos' or a == 'sin' or a == 'tan' or a == 'ctg':
                calc = {'sin': SuperMath.sin, 'cos': SuperMath.cos, 'tan': SuperMath.tan, 'ctg': SuperMath.ctg}
                res = calc[a](float(action.split()[1]))
            else:
                res = calc[a](float(action.split()[0]), float(action.split()[2]))
            print(res)
            if user:
                SuperMath.history(date=str(day), result=str(action + ' = ' + str(res)), userid=user)
        for i in action.split():
            if i == '+':
                result_(i)
            elif i == '/':
                result_(i)
            elif i == '*':
                result_(i)
            elif i == '-':
                result_(i)
            if user:
                if i == 'cos':
                    result_(i)
                elif i == 'sin':
                    result_(i)
                elif i == 'tan':
                    result_(i)
                elif i == 'ctg':
                    result_(i)
                elif i == 'history':
                    print(SuperMath.history_read(userid=user))


def main():
    login_input = (input('please input login, leave blank for anonimus \nor print "exit" to close programm >> '))
    if login_input == 'exit':
        exit(0)
    elif len(login_input) == 0:
        operations(False)
    else:
        if check_user_in_db(login_input):
            password_input = getpass.getpass('password >>>')
            userid = check_user_auth(login_input, password_input)
            if userid:
                try:
                    operations(userid)
                except Exception as e:
                    print(e, type(e))
        else:
            print('New user ', login_input, ' enter')
            register(login_input)


while True:
    main()
