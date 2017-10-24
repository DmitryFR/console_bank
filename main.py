import requests
import threading
lock = threading.Semaphore(1)

def patch_plus(bal,tag,idd):
    r = requests.patch('http://0.0.0.0:5000/users/' + idd, data={'balance': bal}, headers={'If-Match': tag})
    lock.release()
    logFile.write('Plus: HTTP code: ' + str(r.status_code) + '\n')
    if r.status_code == 200:
        print("Сумма успешно добавлена на счет!")
    else:
        print('Ошибка!')

def patch_transfer(bal,tag,idd,oper):
    r = requests.patch('http://0.0.0.0:5000/users/' + idd,json={'operations': oper, 'balance': bal}, headers={'If-Match': tag})
    lock.release()
    logFile.write('Transfer: HTTP code 1: ' + str(r.status_code))
    if r.status_code == 200:
        print('Перевод успешно выполнен!')
    else:
        print("Ошибка!")

print('Здравствуйте!')
print("Добро пожаловать в консольную банковскую систему!")
print("Если вы уже зарегестрированы введите login, если у вас еще нет аккаунта введите reg.")
logFile = open('log.txt', 'a')
current_user = None
while 1:
    key_word = input()
    if key_word == 'login':

        print('Введите ваш логин:')
        login = input()
        print('Введите пароль:')
        password = input()
        #http here
        if login != '':
            # Ищем пользователя с данными соответствующими введенным
            r = requests.get('http://0.0.0.0:5000/users')
            users = r.json()
            if users != []:
                for user in users['_items']:
                    if user['username'] == login and user['password'] == password:
                        current_user = user
                        break
                    else:
                        current_user = None
                # Если нашли  то заходим в основной цикл
                if current_user != None:
                    logFile.write('log in: ' + current_user['username'] + ' '+ current_user['firstname'] + ' ' + current_user['lastname'] + ' HTTP code' + str(r.status_code) + '\n')
                    print("Добро пожаловать," + current_user['firstname'] + ' ' + current_user['lastname'] + '!')
                    break
                else:
                    logFile.write('log in: not successful \n')
                    print('Неправильно указан логин или пароль или пользователь с такими параметрами не существует!')
                    print('Для регистрации введите команду reg, для повторной попытке залогиниться введите login.')
            else:
                logFile.write('log in: not successful \n')
                print('Неправильно указан логин или пароль или пользователь с такими параметрами не существует!')
                print('Для регистрации введите команду reg, для повторной попытке залогиниться введите login.')

        else:
            print('Поле логина пусто!')
            print ('Введите повторно команду login и напишите ваш логин.')

    elif key_word == 'reg':
        print('Введите ваш логин (не меньше 5 символов):')
        login = input()
        print('Введите пароль:')
        password = input()
        print('Введите ваше имя:')
        firstname = input()
        print('Введите вашу фамилию:')
        lastname = input()
        print('Введите сумму на вашем счету:')
        try:
            balance = int(input())
        except ValueError:
            print ("Вы введи буквы вместо цифр, ваш баланс равен 0")
            balance = 0

        info = {'username':login, 'password':password, 'firstname':firstname, 'lastname':lastname, 'balance':balance}
        # Добавляем нового пользователя используя введенные  данные
        r = requests.post("http://0.0.0.0:5000/users", data=info)
        logFile.write('Reg: HTTP code' + str(r.status_code)+ '\n')
        if r.status_code == 422:
            print ("Выбранный вами логин уже используется, или вы не заполнили все поля.")
            print ("Попробуйте еще раз написав команду reg.")
        elif r.status_code == 201:
            # Получаем полную информацию о новом пользователе для дальнейшей работы
            r = requests.get('http://0.0.0.0:5000/users')
            for user in r.json()['_items']:
                if user['username'] == info['username']:
                    current_user = user
            print("Добро пожаловать," + info['firstname'] + ' ' + info['lastname'] + '!')
            logFile.write('Reg + log in: ' + current_user['username'] + ' ' + current_user['firstname'] + ' ' + current_user['lastname'] + ' HTTP code' + str(r.status_code)+ '\n')
            break
    else:
        logFile.write('Reg: incorrect command input\n')
        print ('Введите, пожалуйста корректную команду!')
        print('login для входа, reg для регистрации.')


while 1:
    print('==================================================')
    print("Для дальнейшей работы с сервисом введите команды: balance - для уточнения баланса на счету, transfer - для пересылки средств,")
    print("plus - для пополнения вашего счета, statement - для просмотра истории операций, для выхода введите end.")
    key_word = input()

    if key_word == 'balance':
        # обновляем текущего пользователя и выполняем операцию
        r = requests.get('http://0.0.0.0:5000/users')
        users = r.json()
        for user in users['_items']:
            if user['username'] == current_user['username']:
                bUser = user
                break
        logFile.write('Balance: HTTP code' + str(r.status_code)+ '\n')
        print ('Ваш баланс: '+ str(bUser['balance']))
    elif key_word == 'transfer':
        print ('Введите логин пользователя, кому хотите переcлать деньги:')
        toLogin = input()
        print ('Введите сумму, которую надо перечислить:')
        try:
            amount = int(input())
        except ValueError:
            print('Вы указали буквы вместо цифр, будет переведено 0 у.е.')
            amount = 0
        r = requests.get('http://0.0.0.0:5000/users')
        users = r.json()
        # Получаем обновленные данные текущего и принимаемого перевод пользователей
        for user in users['_items']:
            if user['username'] == current_user['username']:
                current_user = user
                break
        for user in users['_items']:
            if user['username'] == toLogin:
                toUsr = user
                break
            else:
                toUsr = None
                # Если принимающий сущиствует и он не текущий  то выполняем опреацию
        if toUsr != None and toUsr['username'] != current_user['username']:
            if current_user['balance'] - amount < 0:
                logFile.write('Transfer: not enough funds\n')
                print('На счету недостаточно средств!')
            else:
                # Выполнение операции
                current_user['balance'] -= amount
                toUsr['balance'] += amount
                transferInfo = {'host_account':toUsr['username'], 'transmit_account':current_user['username'], 'amount':amount}
                current_user['operations'].append(transferInfo)
                toUsr['operations'].append(transferInfo)
                # Отправка запроса на изменение полей в бд
                # r1 = requests.patch('http://0.0.0.0:5000/users/' + current_user['_id'], json={'operations':current_user['operations'], 'balance':current_user['balance']}, headers={'If-Match':current_user['_etag']})
                # r2 = requests.patch('http://0.0.0.0:5000/users/' + toUsr['_id'], json={'operations':toUsr['operations'], 'balance':toUsr['balance']}, headers= {'If-Match':toUsr['_etag']})
                # logFile.write('Transfer: HTTP code 1: ' + str(r1.status_code) + ' HTTP code 2: ' + str(r2.status_code)+ '\n')
                # if r1.status_code == 200 and r2.status_code == 200:
                #    print('Перевод успешно выполнен!')
                # else:
                #     print ("Ошибка!")
                thread1 = threading.Thread(target=patch_transfer, args=(current_user['balance'], current_user['_etag'], current_user['_id'], current_user['operations']))
                thread1.start()
                lock.acquire()
                thread2 = threading.Thread(target= patch_transfer, args=(toUsr['balance'], toUsr['_etag'], toUsr['_id'], toUsr['operations']))
                thread2.start()
                lock.acquire()

        else:
            logFile.write('Transfer: recieving user is not found\n')
            print('Указанный вами пользователь не был найден!')
    elif key_word == 'plus':
        print('Введите сумму пополнения:')
        try:
            plusAmount = int(input())
        except ValueError:
            print ('Вы ввели буквы вместо цифр, будет зачислено 0 у.е.')
            plusAmount = 0
        # Получение свежей информации о текущем пользователе
        r = requests.get('http://0.0.0.0:5000/users')
        users = r.json()
        for user in users['_items']:
            if user['username'] == current_user['username']:
                current_user = user
                break
        current_user['balance'] += plusAmount
        # Сохранение изменений в бд
        # r = requests.patch('http://0.0.0.0:5000/users/'+current_user['_id'], data= {'balance':current_user['balance']}, headers= {'If-Match':current_user['_etag']})
        # logFile.write('Plus: HTTP code: ' + str(r.status_code)+ '\n')
        # if r.status_code == 200:
        #     print("Сумма успешно добавлена на счет!")
        # else:
        #     print ('Ошибка!')
        thread = threading.Thread(target=patch_plus, args=(current_user['balance'], current_user['_etag'], current_user['_id']))
        thread.start()
        lock.acquire()
    elif key_word == 'statement':
        # Получение свежей информации о текущем пользователе
        r = requests.get('http://0.0.0.0:5000/users')
        logFile.write('Statement: receiving current user HTTP code:' + str(r.status_code)+ '\n')
        users = r.json()
        for user in users['_items']:
            if user['username'] == current_user['username']:
                bUser = user
                break
        # Вывод всех операций аккаунта если они существовали
        if bUser['operations'] != []:
            logFile.write('Statement: output of operations\n')
            for operation in bUser['operations']:
                print ('Пересылка ' + str(operation['amount']) + ' у.е. c счета ' + operation['transmit_account'] + ' на счет '+ operation['host_account'])
        else:
            logFile.write('Statement: No operations found\n')
            print('Операции на текущем аккаунте не найдено!')
    elif key_word =='end':
        print ('Спасибо за использование консольного банка! До свидания!')
        logFile.write('================================================')
        logFile.close()
        break
    else:
        logFile.write('MainCycle: Incorrect command\n')
        print ('Введена некорректная команда!')
