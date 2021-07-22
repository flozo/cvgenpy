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
        rawtext = f.read()
    return rawtext


def format_text(rawtext):
    text = rawtext.split('\n')
    # Remove comment lines
    text = [line for line in text if not '#' in line[:1]]
    # Add LaTeX linebreak \\ before empty line
    for count, line in enumerate(text):
        if line == '':
            text[count-1] = text[count-1] + r'\\'
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
            elif 'enclosure' in config_file:
                generic_enclosure(config_file)
            elif 'letter' in config_file:
                cv.write_letter(config_file)
            else:
                print('[config] Config file name undefined.')
            print('[config] Generic config file {} created.'.format(config_file))
        else:
            print('[config] No config file created.')
            

def generic_enclosure(config_file):
    settings_dict = {
            'name': '/home/user/Document.pdf',
            'reference_letter': '/home/user/Reference_letter.pdf',
            'school_certificate': '/home/user/School_certificate.pdf',
            'bachelor_certificate': '/home/user/Bachelor_certificate.pdf',
            'master_certificate': '/home/user/Master_certificate.pdf',
            'PhD_certificate': '/home/user/PhD_certificate.pdf',
            'MOOC_certificate': '/home/user/MOOC_certificate.pdf',
            }
    with open(config_file, 'w') as f:
        json.dump(settings_dict, f, indent=4)


def mergepdfs(pdflist, target):                                                                                                                                                                                                               
    """
    Concatenate all PDFs
    """
    merger = PdfFileMerger()
    for pdf in pdflist:
        merger.append(pdf)
    merger.write(target)
    merger.close()


def make_link_url(url, shorten_http, shorten_www, label):
    """
    Create clickable link from URL
    """
    if label == '':
        label = url
        if shorten_http is True:
            label = label.replace('https://', '').replace('http://', '')
        if shorten_www is True:
            label = label.replace('www.', '')
    return '\\href{{{}}}{{{}}}'.format(url, label)


def make_link_email(address, label, subject):
    """
    Create clickable link from email address with optional subject
    """
    if label == '':
        label = address
    if subject == '':
        return '\\href{{mailto:{0}}}{{{1}}}'.format(address, label)
    else:
        return '\\href{{mailto:{0}?subject={1}}}{{{2}}}'.format(address, subject, label)

