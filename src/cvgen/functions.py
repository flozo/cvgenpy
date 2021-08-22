#!/usr/bin/env python3

import json
import os
import cvdata as cv
import geometry as geo
import defaults
import pandas as pd
from PyPDF2 import PdfFileMerger
from operator import itemgetter


def read_text(textfile):
    """
    Read text file and write content into variable.
    """
    with open(textfile, 'r', encoding='utf-8') as f:
        rawtext = f.read()
    return rawtext


def format_text(rawtext):
    """
    Convert rawtext lines to list elements and linebreaks to LaTeX linebreaks.
    """
    text = rawtext.split('\n')
    # Remove comment lines
    text = [line for line in text if '#' not in line[:1]]
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


def write_config(config_file, settings_dict):
    """
    Write config file
    """
    with open(config_file, 'w') as f:
        json.dump(settings_dict, f, indent=4)


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
                write_config(config_file, defaults.personal_data_config())
            elif 'company' in config_file:
                write_config(config_file, defaults.generic_company())
            elif 'geo' in config_file:
                write_config(config_file, defaults.geometry_config())
            elif 'enclosure' in config_file:
                write_config(config_file, defaults.generic_enclosure())
            elif 'letter' in config_file:
                defaults.write_letter(config_file)
            elif 'preamble' in config_file:
                write_config(config_file, defaults.generic_preamble())
            elif 'cell_styles' in config_file:
                write_config(config_file, defaults.generic_cell_styles())
            elif 'layers' in config_file:
                write_config(config_file, defaults.generic_layers())
            elif 'skills' in config_file:
                print('No defaults for skills.')
#                write_config(config_file, defaults.generic_layers())
            else:
                print('[config] Config file name undefined.')
            print('[config] Generic config file {} created.'.format(config_file))
        else:
            print('[config] No config file created.')


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


def replace_strings(translation_dict, string):
    """
    Replace all occurences of keys in translation_dict in string by values.
    """
    for key, value in translation_dict.items():
        string = string.replace(key, value)
    return string


def parse_layers(layers_dict):
    """
    Create TikZ layer declarations from layer dictionary.
    """
    l = []
    for key, value in layers_dict.items():
        # Create list with layer position and name
        l.append([value['position'], value['name']])
    # Add main layer
    l.append([0, 'main'])
    # Sort by position
    l.sort(key=itemgetter(0))
    # Create layer order
    set_layers = '\\pgfsetlayers{'
    for layer in l:
        set_layers = set_layers + layer[1] + ', '
    set_layers = set_layers[:-2] + '}'
    # Create declare-layers commands
    latex = []
    for layer in l:
        # Exclude 'main' from layer declaration
        if 'main' not in layer:
            latex.append('\\pgfdeclarelayer{{{}}}'.format(layer[1]))
    latex.append(set_layers)
    return latex


def make_skill_circles(level, maxlevel):
    """
    Generate skill-circle row.
    """
    if level == maxlevel:
        return '\\tikz{\\pic {skillmax};}'
    elif level == 0:
        return '\\tikz{\\pic {skillmin};}'
    else:
        return '\\tikz{{\\pic {{skill={{{}}}{{{}}}}};}}'.format(level, level+1)


def make_level_numeric(level, maxlevel):
    """
    Generate numeric skill level string.
    """
    return '{}/{}'.format(level, maxlevel)


def make_section_header_left(dataframe):
    """
    Keep group name in first row only and replace duplicates with empty string.
    """
    first_row = dataframe.drop_duplicates(subset=['group'], keep='first')
    body = dataframe.drop(index=dataframe.index[0], axis=0)
    body['group'] = ''
    return pd.concat([first_row, body])


def make_section_header_top(dataframe):
    """Make separate row for group name and return new dataframe."""
    first_row = dataframe.iloc[0]
    return pd.concat([first_row, dataframe])


def make_table(dataframe, section_header_style, item_style, item_separator):
    """Rearrange dataframe with respect to selected section style."""
    if section_header_style == 'left' and item_style == 'multirow':
        return pd.concat([make_section_header_left(dataframe)])
    elif section_header_style == 'left' and item_style == 'onerow':
        return dataframe.groupby(['group'], as_index=True).agg({'name': item_separator.join, 'level_numeric': item_separator.join, 'circles': item_separator.join})
    elif section_header_style == 'top' and item_style == 'multirow':
        return pd.concat([make_section_header_top(dataframe)])
