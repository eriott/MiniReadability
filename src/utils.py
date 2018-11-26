import re
import textwrap


def match_items(item, list):
    matches = [key for key in list if re.compile(key).match(item)]
    return None if len(matches) == 0 else matches[0]


def match_keys(item, dict):
    matches = [(key, value) for key, value in dict.items() if re.compile(key).match(item)]
    return None if len(matches) == 0 else matches[0]


def wrap(text, max_length):
    return '\n'.join(['\n'.join(textwrap.wrap(x, width=max_length)) for x in text.split('\n')])
