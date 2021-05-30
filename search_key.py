#!python
# encoding: utf-8

# Created by JG at 2020-08-28


import re
import sys

"""
script for searching a windows key in bios bin file

usage: 
search_key.exe file.bin
"""


class SearchKey:
    def __init__(self):
        version = "1.1.1.0"
        date = "23.09.2020"
        self.filename = None
        self.bytes = None
        self.key = None
        self.with_new_key = None

    def open_file(self, filename):
        with open(filename, 'rb') as file:
            self.bytes = file.read()

    def search_key(self):
        pattern = (b'[A-Z\d]{5}-[A-Z\d]{5}-[A-Z\d]{5}-[A-Z\d]{5}-[A-Z\d]{5}')
        p = re.compile(pattern)
        for i in p.finditer(self.bytes):
            # print(i[0].decode("utf-8"))
            self.key = i[0]
            return self.key
        return None

    def print_bin(self):
        print(self.bytes)

    def replace_key(self, new_key):
        # new_key as a string later is coded to bytes
        # TODO needed a checking if a self.key is not None
        self.with_new_key = self.bytes.replace(self.key, new_key.encode())

    def save_file(self, file_name):
        with open(file_name, 'w+b') as file:
            file.write(self.with_new_key)


if __name__ == "__main__":
    app = SearchKey()
    app.open_file(sys.argv[1])
    app.search_key()
    app.print_bin()
    app.replace_key("11111-22222-33333-44444-55555")
