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
    """
    Convert rawtext lines to list elements and
    linebreaks to LaTeX linebreaks.
    """
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
    """
    Check if config directory exists. If not, ask for creating one.
    """
    if not os.path.isdir(config_dir):
        print('[config] Config directory {} not found.'.format(config_dir))
        create_config_dir = input('[config] Create config directory {} ? (Y/n): '.format(config_dir))
        if create_config_dir == 'Y':
            os.makedirs(config_dir)
            print('[config] Config directory {} created.'.format(config_dir))
        else:
            print('[config] No config directory created.')


def check_config_file(config_file):
    """
    Check if config files exist. If not, ask for creating
    config files with generic settings.
    """
    if not os.path.isfile(config_file):
        print('[config] Config file {} not found.'.format(config_file))
        create_config_dir = input('[config] Create generic config file {} ? (Y/n): '.format(config_file))
        if create_config_dir == 'Y':
            if 'cvdata' in config_file:
                cv.write_config(config_file)
            elif 'company' in config_file:
                generic_company(config_file)
            elif 'geo' in config_file:
                geo.write_config(config_file)
            elif 'enclosure' in config_file:
                generic_enclosure(config_file)
            elif 'letter' in config_file:
                cv.write_letter(config_file)
            elif 'preamble' in config_file:
                generic_preamble(config_file)
            elif 'cell_styles' in config_file:
                generic_cell_styles(config_file)
            else:
                print('[config] Config file name undefined.')
            print('[config] Generic config file {} created.'.format(config_file))
        else:
            print('[config] No config file created.')
            

def generic_enclosure(config_file):
    """
    Define generic enclosure list.
    """
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


def generic_preamble(config_file):
    """
    Define generic LaTeX preamble
    """
    documentclass = {
            'standalone': '12pt, tikz, multi, crop',
            }
    packages = {
            'inputenc': 'utf8',
            'fontenc': 'T1',
            'babel': 'german',
            'hyperxmp': '',
            'FiraSans' : 'sfdefault, scaled=1.0098',
            'newtxsf': '',
            'fontawesome5': '',
            'csquotes': 'german=quotes',
            'enumitem': '',
            'microtype': 'activate={true, nocompatibility}, final, tracking=true, kerning=true, spacing=true, factor=1100, stretch=8, shrink=8',
            'tikz': '',
            'hyperref': '',
            }
    settings = {
            'usetikzlibrary': 'positioning, math, colorbrewer, backgrounds, matrix',
            'standaloneenv': 'tikzpicture',
            'hypersetup': 'colorlinks=true, urlcolor=Blues-K',
            }
    preamble = {
            'documentclass': documentclass,
            'packages': packages,
            'settings': settings,
            }
    with open(config_file, 'w') as f:
        json.dump(preamble, f, indent=4)


def generic_cell_styles(config_file):
    """
    Define generic TikZ cell styles
    """
    cell_styles = {
            'cell1': {
                'name': 'cell1',
                'xsep': 16,
                'ysep': 10,
                'align': 'right',
                'minimum_width': 2.0,
                'minimum_height': 0.5,
                'text_width': 4.0,
                'text_height': 0.25,
                },
            'cell2': {
                'name': 'cell2',
                'xsep': 2,
                'ysep': 10,
                'align': 'left',
                'minimum_width': 1.5,
                'minimum_height': 0.5,
                'text_width': 9.5,
                'text_height': 0.25,
                },
            'cell3': {
                'name': 'cell3',
                'xsep': 16,
                'ysep': 4,
                'align': 'center',
                'minimum_width': 0.6,
                'minimum_height': 0.5,
                'text_width': 0.4,
                'text_height': 0.25,
                },
            'cell4': {
                'name': 'cell4',
                'xsep': 2,
                'ysep': 4,
                'align': 'left',
                'minimum_width': 1.0,
                'minimum_height': 0.5,
                'text_width': 7.8,
                'text_height': 0.25,
                },
            'cell5': {
                'name': 'cell5',
                'xsep': 0,
                'ysep': 6,
                'align': 'left',
                'minimum_width': 0.6,
                'minimum_height': 0.5,
                'text_width': 4.5,
                'text_height': 0.25,
                },
            'cell6': {
                'name': 'cell6',
                'xsep': 0,
                'ysep': 6,
                'align': 'right',
                'minimum_width': 1.0,
                'minimum_height': 0.5,
                'text_width': 2.0,
                'text_height': 0.25,
                },
            'cell7': {
                'name': 'cell7',
                'xsep': 8,
                'ysep': 10,
                'align': 'left',
                'minimum_width': 1.0,
                'minimum_height': 0.5,
                'text_width': 5.0,
                'text_height': 0.25,
                },
            'cell8': {
                'name': 'cell8',
                'xsep': 8,
                'ysep': 6,
                'align': 'right',
                'minimum_width': 0.6,
                'minimum_height': 0.5,
                'text_width': 7.8,
                'text_height': 0.25,
                },
            'cell9': {
                'name': 'cell9',
                'xsep': 0,
                'ysep': 6,
                'align': 'center',
                'minimum_width': 0.4,
                'minimum_height': 0.5,
                'text_width': 0.4,
                'text_height': 0.25,
                },
            'cell10': {
                'name': 'cell10',
                'xsep': 16,
                'ysep': 4,
                'align': 'right',
                'minimum_width': 2.0,
                'minimum_height': 0.5,
                'text_width': 4.0,
                'text_height': 0.25,
                },
            'cell11': {
                'name': 'cell11',
                'xsep': 2,
                'ysep': 4,
                'align': 'left',
                'minimum_width': 1.5,
                'minimum_height': 0.5,
                'text_width': 9.5,
                'text_height': 0.25,
                },
            'cell12': {
                'name': 'cell12',
                'xsep': 2,
                'ysep': 4,
                'align': 'left',
                'minimum_width': 1.5,
                'minimum_height': 0.5,
                'text_width': 4.5,
                'text_height': 0.25,
                },
            }
    with open(config_file, 'w') as f:
        json.dump(cell_styles, f, indent=4)


def generic_company(config_file):
    """
    Define generic company data
    """
    company_data = {
            "name": "Company",
            "attention": "James Jones",
            "street": "Street name",
            "house": "987b",
            "postal_code": "67890",
            "city": "City",
            "country": "Country",
            "position": "Position",
            "color_main": "blue",
            "color_accent": "yellow"
            }
    with open(config_file, 'w') as f:
        json.dump(company_data, f, indent=4)


def mergepdfs(pdflist, target):                                                                                                                                                                                                               
    """
    Concatenate all PDFs.
    """
    merger = PdfFileMerger()
    for pdf in pdflist:
        merger.append(pdf)
    merger.write(target)
    merger.close()


def make_link_url(url, shorten_http, shorten_www, label):
    """
    Create clickable link from URL.
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
    Create clickable link from email address with optional subject.
    """
    if label == '':
        label = address
    if subject == '':
        return '\\href{{mailto:{0}}}{{{1}}}'.format(address, label)
    else:
        return '\\href{{mailto:{0}?subject={1}}}{{{2}}}'.format(address, subject, label)


def makelist(string):
    """
    Convert string to list if first and last character are [ and ], respectively.
    """
    if len(string) > 0 and string[0] == '[' and string[-1] == ']':
        return string[1:-1].split(';')
    else:
        return string

