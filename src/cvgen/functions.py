#!/usr/bin/env python3

import json
import os
import cvdata as cv
import geometry as geo

def read_config(config_file):
    """
    Read JSON config file and write content into nested dictionary.
    """
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config


def check_config_dir(config_dir):
#    path_or_file = os.path.expanduser(path_or_file)
#    config_dir = os.path.dirname(path_or_file)
#    config_file = os.path.basename(path_or_file)
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
            else:
                print('[config] Config file name undefined.')
            print('[config] Generic config file {} created.'.format(config_file))
        else:
            print('[config] No config file created.')
 