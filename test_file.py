import unittest
import requests

class TestConsoleBank(unittest.TestCase):
    fser = {}
    def test_a (self):
        # testing post request
        test_data = {'username': 'testt', 'firstname': 'testt', 'lastname': 'testt', 'balance':1000, 'password':'testt'}
        r = requests.post('http://0.0.0.0:5000/users', data=test_data)
        self.assertEqual(r.status_code, 201)

    def test_b(self):
        # testing get request
        r = requests.get('http://0.0.0.0:5000/users')
        self.assertEqual(r.status_code, 200)

        self.assertEqual(type (r.json()), type({}))

    def test_c(self):
        # testing patch request
        r = requests.get('http://0.0.0.0:5000/users')
        users = r.json()
        for user in users['_items']:
            if user['username'] == 'testt':
                self.fser = user
                break
        r = requests.patch('http://0.0.0.0:5000/users/' + self.fser['_id'], data={'balance': 2000}, headers={'If-Match': self.fser['_etag']})
        self.assertEqual(r.status_code, 200)

    def test_d(self):
        # testing patch request with list parameter
        testList = [{'host_account':'testt', 'transmit_account':'testc', 'amount':100}, {'host_account':'testc', 'transmit_account':'testt', 'amount':100}, {'host_account':'testt', 'transmit_account':'testc', 'amount':200}]
        r = requests.get('http://0.0.0.0:5000/users')
        users = r.json()
        for user in users['_items']:
            if user['username'] == 'testt':
                self.fser = user
                break
        r = requests.patch('http://0.0.0.0:5000/users/' + self.fser['_id'], json={'operations': testList}, headers={'If-Match': self.fser['_etag']})
        self.assertEqual(r.status_code, 200)
    def test_e(self):
        for i in range(100):
            r=requests.get('http://0.0.0.0:5000/users')


    # def test_f(self):
    #     # testing
    #     r = requests.get('http://0.0.0.0:5000/users')
    #     users = r.json()
    #     for user in users['_items']:
    #         if user['username'] == 'testt':
    #             r = requests.delete('http://0.0.0.0:5000/users/' + user['_id'], headers={'If-Match': user['_etag']})
    #             self.assertEqual(r.status_code, 204)
    #             break

if __name__ == '__main__':
    unittest.main()


