#!/usr/bin/env python3

import argparse
import os
import requests

TOKEN = os.environ['SECRET_KEY']


def get_user_id():
    parser = argparse.ArgumentParser(description='VK API script', epilog='enjoy ;)')
    parser.add_argument('-id', action='store', dest='user_id', help='User id in VK', type=int)
    args = parser.parse_args()
    return args.user_id


def create_a_query(user_id):
    if user_id is None:
        return 'return API.users.get({"user_ids": API.friends.getOnline()});'
    else:
        return 'return API.users.get({"user_ids": API.friends.getOnline({"user_id":%s})});' % user_id


def make_vk_request(execute_code):
    url = 'https://api.vk.com/method/execute'
    parameters = {'code': execute_code, 'access_token': TOKEN, 'v': '5.85'}
    response = requests.get(url, params=parameters)
    json_object = response.json()
    return json_object


def get_errors_msg(json_object):
    errors_msg = json_object['execute_errors'][0]['error_msg']
    return errors_msg


def get_names(json_object):
    user_list = json_object['response']
    names = []
    for item in user_list:
        names.append(item['first_name'] + ' ' + item['last_name'])
    return names


def make_friends_list(names):
    if names:
        return 'Friends online: %s' % ', '.join(names)
    else:
        return 'No friends online'


if __name__ == '__main__':
    user_id = get_user_id()
    query = create_a_query(user_id)
    response_content = make_vk_request(query)
    if response_content.get('execute_errors'):
        print(get_errors_msg(response_content))
    else:
        friends_online = make_friends_list(get_names(response_content))
        print(friends_online)