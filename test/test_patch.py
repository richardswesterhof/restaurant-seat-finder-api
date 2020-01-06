import requests
import sys
import json
from test import __site
from test_login import test_login

def test_patch():
    dict = {
        'free_seats': 19, 'name': 'TEST3000',
                     'address': {'street': 'NEWNEWNEW', 'str222': None}
    }
    return requests.patch(__site + '/places/1', json=dict)

def test_login_patch():
    dict = {
        'free_seats': 9
    }
    token = json.loads(test_login().content)["token"]
    return requests.patch(__site + '/places/1', json=dict, headers={'Authorization': 'Bearer %s' % token})


def test_current():
    token = json.loads(test_login().content)["token"]
    return requests.get(__site + '/current-place', headers={'Authorization': 'Bearer %s' % token})

if __name__ == '__main__':
    try:
        response = test_login_patch()
    except KeyError:
        print("No such value")
        sys.exit(1)

    print(f'status code: {response.status_code}\n')
    print('headers: \n')
    for header in response.headers:
        print(f'    {header}: {response.headers[header]}\n')
    print(f'content:\n{response.content}')
