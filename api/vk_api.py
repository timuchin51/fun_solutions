#!/usr/bin/env python3

import os
import requests
from sys import argv

token = os.environ['SECRET_KEY']


def create_a_query(com_line_arguments):
    if len(com_line_arguments) == 1:
        return 'return API.users.get({"user_ids": API.friends.getOnline()});'
    elif len(com_line_arguments) > 2:
        print('Only one arguments is needed')
    elif com_line_arguments[1].isdecimal():
        return 'return API.users.get({"user_ids": API.friends.getOnline({"user_id":%s})});' % com_line_arguments[1]
    else:
        print('Input right User Id')
        return False


def get_request_api(execute_code):
    url = 'https://api.vk.com/method/execute'
    parameters = {'code': execute_code, 'access_token': token, 'v': '5.85'}
    response = requests.get(url, params=parameters)
    json_object = response.json()
    return json_object


def get_errors_msg(json_object):
    if json_object.get('execute_errors'):
        errors_msg = json_object['execute_errors'][0]['error_msg']
        print(errors_msg)


def get_names(json_object):
    user_list = json_object['response']
    names = []
    for item in user_list:
        names.append(item['first_name'] + ' ' + item['last_name'])
    if names:
        return 'Friends online: %s' % ', '.join(names)
    else:
        return 'No friends online'


if __name__ == '__main__':
    query = create_a_query(argv)
    if query:
        request_api = get_request_api(query)
        get_errors_msg(request_api)
        friends_online = get_names(request_api)