#!/usr/bin/env python3

import json
import os
import cvdata as cv
import geometry as geo
from PyPDF2 import PdfFileMerger


def read_text(textfile):
    """
    Read text file and write content into variable.
    """
    with open(textfile, 'r', encoding='utf-8') as f:
        text = f.readlines()
    print(text)
    return text


def format_text(text):
    for count, line in enumerate(text):
        if line[0] == '#':
            text[count] = ''
        if line == '\n':
            text[count-1] = text[count-1].replace('\n', r'\\')
    return text


def read_config(config_file):
    """
    Read JSON config file and write content into nested dictionary.
    """
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config


def check_config_dir(config_dir):
    if not os.path.isdir(config_dir):
        print('[config] Config directory {} not found.'.format(config_dir))
        create_config_dir = input('[config] Create config directory {} ? (Y/n): '.format(config_dir))
        if create_config_dir == 'Y':
            os.makedirs(config_dir)
            print('[config] Config directory {} created.'.format(config_dir))
        else:
            print('[config] No config directory created.')


def check_config_file(config_file):
    if not os.path.isfile(config_file):
        print('[config] Config file {} not found.'.format(config_file))
        create_config_dir = input('[config] Create generic config file {} ? (Y/n): '.format(config_file))
        if create_config_dir == 'Y':
            if 'cvdata' in config_file:
                cv.write_config(config_file)
            elif 'geo' in config_file:
                geo.write_config(config_file)
            elif 'letter' in config_file:
                cv.write_letter(config_file)
            else:
                print('[config] Config file name undefined.')
            print('[config] Generic config file {} created.'.format(config_file))
        else:
            print('[config] No config file created.')
            

def mergepdfs(pdflist, target):                                                                                                                                                                                                               
    """
    Concatenate all PDFs
    """
    merger = PdfFileMerger()
    for pdf in pdflist:
        merger.append(pdf)
    merger.write(target)
    merger.close()

