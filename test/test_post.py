import requests
import sys
import json
from test import __site

def test_post():
    dict = {'name': 'HgGGGDfsf', 'address':
        {'street': 'Coolstraat', 'house_number': '2', 'postcode': '9321CV', 'city': 'Groningen', 'country': 'Netherlands'},
     'total_seats': 20, 'free_seats': 1}
    return requests.post(__site + '/places', json=dict)


if __name__ == '__main__':
    try:
        response = test_post()
        # response = globals()[sys.argv[1]]()
    except KeyError:
        print("No such value")
        sys.exit(1)

    print(f'status code: {response.status_code}\n')
    print('headers: \n')
    for header in response.headers:
        print(f'    {header}: {response.headers[header]}\n')
    print(f'content:\n{response.content}')
