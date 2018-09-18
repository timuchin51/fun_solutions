#!/usr/bin/env python3

from settings import access_token as token
import requests


code = 'return API.users.get({"user_ids": API.friends.getOnline()}); '


def get_request_api(execute_code):
    url = 'https://api.vk.com/method/execute'
    parameters = {'code': execute_code, 'access_token': token, 'v': '5.85'}
    response = requests.get(url, params=parameters)
    json_object = response.json()
    return json_object


def get_names(json_object):
    user_list = json_object['response']
    names = ['Friends online: ']
    for item in user_list:
        names.append(item['first_name']+item['last_name'])
    print(names)

if __name__ == '__main__':

    j = get_request_api(code)
    get_names(j)
