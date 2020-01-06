import requests
import sys
import json
from test import __site
from test_login import test_login
import test_post

def test_delete():
    token = json.loads(test_login(test_post.username, test_post.password).content)["token"]
    return requests.delete(__site + '/places/4', headers={'Authorization': 'Bearer %s' % token})


if __name__ == '__main__':

    response = test_delete()

    print(f'status code: {response.status_code}\n')
    print('headers: \n')
    for header in response.headers:
        print(f'    {header}: {response.headers[header]}\n')
    print(f'content:\n{response.content}')
