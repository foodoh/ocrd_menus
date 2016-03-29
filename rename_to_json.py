# -*- coding: utf-8 -*-
# @Author: Tasdik Rahman
# @Date:   2016-03-29 19:52:36
# @Last Modified by:   Tasdik Rahman
# @Last Modified time: 2016-03-29 19:56:19

import os

PATH = os.path.abspath('.')
FILE_DIR = os.path.join(PATH, 'menu_text')

def rename_process():
    for file in os.listdir(FILE_DIR):
        filename, file_ext = os.path.splitext(file)
        json_name = filename + '.json'
        os.rename(os.path.join(
                FILE_DIR, file), os.path.join(FILE_DIR, json_name))

def main():
    rename_process()

if __name__ == "__main__":
    main()