import re


def match_items(item, list):
    matches = [key for key in list if re.compile(key).match(item)]
    return None if len(matches) == 0 else matches[0]


def match_keys(item, dict):
    matches = [(key, value) for key, value in dict.items() if re.compile(key).match(item)]
    return None if len(matches) == 0 else matches[0]
