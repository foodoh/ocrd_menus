# -*- coding: utf-8 -*-
# @Author: Tasdik Rahman
# @Date:   2016-03-14
# @Last Modified by:   Tasdik Rahman
# @Last Modified time: 2016-03-25 21:06:46
# @MIT License
# @http://tasdikrahman.me
# @https://github.com/prodicus

import os

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import PlaintextCorpusReader
from rmgarbage import Rmgarbage

PROJECT_DIR = os.path.abspath(os.path.join('.'))
DATA_DIR = os.path.join(PROJECT_DIR, 'first_600_all_menus')
NEW_DATA_DIR = os.path.join(PROJECT_DIR, 'cleaned_600_menus')

rmobject = Rmgarbage()


def clean_text():
    """
    Will read the text from the files inside the 'DATA_DIR' and then pass the
    strings through the functions in the class 'Rmgarbage'. 

    The cleaned menus will be stored in 'NEW_DATA_DIR'
    """
    pass



def main():
    clean_text()

if __name__ == "__main__":
    main()