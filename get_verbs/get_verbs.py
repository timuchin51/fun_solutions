#!/usr/bin/env python3

import re


def rewriting_file():
    with open('vocabulary.txt', 'r') as raw_data, open('verbs.txt', 'w') as finished_data:
        index = 0
        for line in raw_data:
            verbs_list = find_verbs(line)
            if verbs_list:
                verbs = verb_conjugations(verbs_list)
                index += 1
                finished_data.write(str(index)+') Глагол: %s.' % ', '.join(verbs)+'\n')


def find_verbs(text):
    verbs = re.match('[А-Я]+(АТЬ|ИТЬ|СЯ|СТИ|ЕЧЬ|УТЬ|ЕТЬ)(?![А-Я]),[\w\s,-]*(?=;)', text)
    if verbs:
        verbs = verbs.group().split(',')
    return verbs


def verb_conjugations(verbs_list):
    formatted_list = []
    for verb in verbs_list:
        if '-' not in verb:
            formatted_list.append(verb.lstrip().capitalize())
        elif verb[2] == 'т':
            result = re.sub('([А-Я]+)Т[А-Я]+ТЬ', r'\1'+verb[2:], verbs_list[0])
            formatted_list.append(result.capitalize())
        else:
            regex_pattern = verb[2].upper()
            result = re.sub('([А-Я]+)'+regex_pattern+'(?!'+regex_pattern+')([А-Я]+)', r'\1'+verb[2:], verbs_list[0])
            formatted_list.append(result.capitalize())
    return formatted_list


if __name__ == '__main__':
    rewriting_file()