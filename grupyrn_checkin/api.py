import requests

from . import config

_base_url = config.get('api_url')
_key = config.get('api_key')


def current_events():
    response = requests.get('{}/{}'.format(_base_url, 'currentevents/'), headers={'Authorization': 'Token ' + _key})
    return response.ok, response.json()


def event_check(uuid, check):
    data = {'attendee': uuid, 'check': check}
    response = requests.post('{}/{}'.format(_base_url, 'check/'), json=data, headers={'Authorization': 'Token ' + _key})
    return response.ok, response.json()


def subevent_checkout(uuid):
    data = {'attendee': uuid}
    response = requests.post('{}/{}'.format(_base_url, 'subeventcheckoutall/'), json=data, headers={'Authorization': 'Token ' + _key})
    return response.ok, response.json()
