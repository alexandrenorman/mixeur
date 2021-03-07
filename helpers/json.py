# -*- coding: utf-8 -*-

from re import compile


def camel_to_snakecase(name):
    """
    Convert a name from camel case convention to snakecase lower case convention.
    Args:
        name (str): name in camel case convention.
    Returns:
        name in snakecase lowercase convention.
    """
    camel_pat = compile(r"([A-Z])")
    return camel_pat.sub(lambda x: "_" + x.group(1).lower(), name)


def snakecase_to_camel(name):
    """
    Convert a name from snakecase lower case convention to camel case convention.
    Args:
        name (str): name in snakecase lowercase convention.
    Returns:
        Name in camel case convention.
    """
    under_pat = compile(r"_([a-z])")
    return under_pat.sub(lambda x: x.group(1).upper(), name)


def change_list_naming_convention(d, convert_function):
    new = []
    for item in d:
        new.append(change_dict_naming_convention(item, convert_function))
    return new


# http://lopezpino.com/2015/11/12/python-dicts-naming-conventions/
def change_dict_naming_convention(d, convert_function):
    """
    Convert a nested dictionary from one convention to another.
    Args:
        d (dict): dictionary (nested or not) to be converted.
        convert_function (func): function that takes the string in one convention and returns it in the other one.
    Returns:
        Dictionary with the new keys.
    """
    if isinstance(d, list):
        return change_list_naming_convention(d, convert_function)

    if isinstance(d, str) or isinstance(d, int) or isinstance(d, float) or d is None:
        return d

    new = {}
    for k, v in d.items():
        new_v = v
        if isinstance(v, dict):
            new_v = change_dict_naming_convention(v, convert_function)
        elif isinstance(v, list):
            new_v = list()
            for x in v:
                new_v.append(change_dict_naming_convention(x, convert_function))
        new[convert_function(k)] = new_v
    return new
