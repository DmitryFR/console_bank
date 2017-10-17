import unittest
import requests

class TestConsoleBank(unittest.TestCase):
    fser = {}
    # Поскольку основной функцией сервиса является работа с базой данных (создание новых записей, выбор уже имеющейся
    # информации из базы, изменение некоторых полей в уже сохраненных записях), то для уверенности в правильной работе сервиса
    # необходимо проверить работоспособность POST, GET, PATCH запросов
    def test_a (self):
        # testing post request
        # Функциональный тест, проверяет добавление нового пользователя в систему со всеми необходимыми  параметрами
        # Ожидается позитивный результат, код добавления в базу 201, что означает корректное добавление нового пользователя.
        test_data = {'username': 'testt', 'firstname': 'testt', 'lastname': 'testt', 'balance':1000, 'password':'testt'} # PreCondition
        r = requests.post('http://0.0.0.0:5000/users', data=test_data) # TestCase Description
        self.assertEqual(r.status_code, 201)

    def test_b (self):
        # testing post request
        # Функциональный тест, проверяет добавление нового пользователя в систему, со всеми необходимыми параметрами, но с уже использованным логином
        # Ожидается негативный результат, код ошибки при добавлении в базу 422, что означает невозможность добавить пользователя с уже взятым логином.
        test_data = {'username': 'testt', 'firstname': 'testt', 'lastname': 'testt', 'balance':1000, 'password':'testt'} # PreCondition
        r = requests.post('http://0.0.0.0:5000/users', data=test_data) # TestCase Description
        self.assertEqual(r.status_code, 422)

    def test_c(self):
        # testing get request
        # Функциональный тест, проверяет выгрузку всех ранее добавленных данных из базы
        # Ожидается позитивный результат, код успешного выполнения 200, что означает корректную выгрузку данных
        r = requests.get('http://0.0.0.0:5000/users') # Test case descripton, PreConditional  - test_a
        self.assertEqual(r.status_code, 200)


    def test_d(self):
        # testing patch request
        # Функциональный тест, проверяет возможность изменения значений некоторых полей у уже существующего пользователя
        # Изменение данных возможно только при совпадении специального тега etag, который меняется при изменении содержимого ресурса
        # что позволяет оптимально упарвлять многопоточностью. Если etag не совпадает изменения не записываются в базу
        # Ожидается позитивный результат, код успешного выполнения 200, что означает успешное изменение некоторых полей
        r = requests.get('http://0.0.0.0:5000/users') #
        users = r.json()                              #
        for user in users['_items']:                  # PreConditional
            if user['username'] == 'testt':           #
                self.fser = user                      #
                break
        r = requests.patch('http://0.0.0.0:5000/users/' + self.fser['_id'], data={'balance': 2000}, headers={'If-Match': self.fser['_etag']}) # Test case description
        self.assertEqual(r.status_code, 200)

    def test_e(self):
        # Нагрузочный тест, проверяет способность базы данных ответить на множество запросов к одному ресурсу
        # Тест необходим для имитации работы определенного количества пользователей на ресурсе
        # Ожидается позитивный результат, код успешного выполнения 200
        for i in range(100): #PreConditional
            r=requests.get('http://0.0.0.0:5000/users')# Test case description
            self.assertEqual(r.status_code, 200)


    def test_f(self):
        # testing delete request
        # Функциональный тест, проверяющий возможность удалить пользователя с указанным логином
        # Такое осуществимо только при совпадении специального тега etag
        # Тест необходим для возврата системы в первоначальное состояние, до проведения тестирования
        # Ожидается позитивный результат, код успешного удаления 204, что означает корректное удаления пользователя из базы
        # является post conditions для выше приведенных тестов
        r = requests.get('http://0.0.0.0:5000/users') # Preconditional
        users = r.json()
        for user in users['_items']:
            if user['username'] == 'testt':
                r = requests.delete('http://0.0.0.0:5000/users/' + user['_id'], headers={'If-Match': user['_etag']}) #Test Case description
                self.assertEqual(r.status_code, 204)
                break
    def test_h (self):
        # testing post request
        # Функциональный тест, проверяет добавление нового пользователя в систему с неполным набором парамтеров
        # Ожидается негативный результат, код ошибки добавления в базу 422, что означает недостататочное колиичество указанных параметров для добавления в базу.
        test_data = {'username': 'testt', 'password':'testt'} # PreCondition
        r = requests.post('http://0.0.0.0:5000/users', data=test_data) # TestCase Description
        self.assertEqual(r.status_code, 422)

if __name__ == '__main__':
    unittest.main()


