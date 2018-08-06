import requests

import config

_base_url = config.get('api_url')
_key = config.get('api_key')


def current_events():
    response = requests.get('{}/{}'.format(_base_url, 'currentevent'), headers={'Authorization': 'Token ' + _key})
    return response.ok, response.json()


def event_check(member_data, event, check):
    try:
        if not member_data.get('cpf'):
            del member_data['cpf']
    except Exception:
        pass

    data = {'member': member_data, 'check': check, 'event': event['id']}
    response = requests.post('{}/{}'.format(_base_url, 'check/'), json=data, headers={'Authorization': 'Token ' + _key})

    return response.ok, response.json()
