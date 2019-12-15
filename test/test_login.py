import requests
import sys
import json
from test import __site


def test_login():
    dict = {'username': 'user1', 'password': 'password1'}
    return requests.post(__site + '/login', json=dict)


if __name__ == '__main__':

    response = test_login()
    print(f'status code: {response.status_code}\n')
    print('headers: \n')
    for header in response.headers:
        print(f'    {header}: {response.headers[header]}\n')
    print(f'content:\n{response.content}')
