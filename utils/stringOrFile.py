import os


def string_or_path(string_or_file):
    if os.path.isfile(string_or_file):
        ret = open(string_or_file, 'r').read()
    else:
        ret = string_or_file
    return ret