import requests
import time


def req(url):
    for i in range(1, 26):
        forma = {
            'email': str(f'{"test"}{i}@{"gmail.com"}'),
            'password': i,
        }
        response = requests.post(url, data=forma)

        if response.status_code == 429:
            time.sleep(60)
        if response.status_code == 200:
            return forma


if __name__ == '__main__':
    req('http://127.0.0.1:5000/login')
