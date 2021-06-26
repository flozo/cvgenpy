#!/usr/bin/env python3

import json

class Box(object):
#    def __init__(self, dict_box):
    def __init__(self, height, width, color):
        self.height = height
        self.width = width
        self.color = color
#        self.size = dict_box['size']
#        self.color = dict_box['color']


class Layout(object):
    def __init__(self, dict_layout):
        self.height = dict_layout['height']
        self.width = dict_layout['width']
        self.background_color = dict_layout['background_color']
        self.box_top = dict_layout['box_top']
        self.box_bottom = dict_layout['box_bottom']
        self.box_left = dict_layout['box_left']
        self.box_right = dict_layout['box_right']
#        super().__init__(size, color)


class SkillCircle(object):
    def __init__(self, dict_skill_circle):
#    def __init__(self, radius, fillcolor, linecolor, showline=False):
        self.radius = dict_skill_circle['radius']
        self.fillcolor = dict_skill_circle['fillcolor']
        self.linecolor = dict_skill_circle['linecolor']
        self.showline = dict_skill_circle['showline']


class SkillLayout(object):
    def __init__(self, dict_skill_layout):
#    def __init__(self, SkillCircle, number=5, distance=5):
#        self.skillcircle = SkillCircle
        self.number = dict_skill_layout['number']
        self.distance = dict_skill_layout['distance']
#        super().__init__(radius=2, fillcolor, linecolor, showline=False)


def write_config(config_dir):
    """
    Create geometry config file with generic settings.
    Settings are defined as nested dictionary and parsed to a JSON file.
    """
    settings_dict = {
            'Layout': {
                'height': 29.7,
                'width': 21.0,
                'background_color': 'white',
                'box_top': False,
                'box_bottom': False,
                'box_left': True,
                'box_right': False,
                },
            'Boxes': {
                'box_top': {
                    'size': 15,
                    'color': 'Greys-J',
                    },
                'box_bottom': {
                    'size': 15,
                    'color': 'Greys-J',
                    },
                'box_left': {
                    'size': 15,
                    'color': 'Greys-J',
                    },
                'box_right': {
                    'size': 15,
                    'color': 'Greys-J',
                    },
                },
            'SkillCircle': {
                'radius': 2,
                'fillcolor': 'Reds-E',
                'linecolor': 'black',
                'showline': False,
                },
            'SkillLayout': {
                'number': 5,
                'distance': 5,
                },
            }
    with open(config_dir, 'w') as f:
        json.dump(settings_dict, f, indent=4)

def read_config(config_file):
    """
    Read JSON config file and write content into nested dictionary.
    """
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config


def split_config(config):
    """
    Split dictionary from JSON config file into sub dictionaries.
    """
    dict_layout = config['Layout']
    dict_box = config['Boxes']
    dict_box_top = dict_box['box_top']
    dict_box_bottom = dict_box['box_bottom']
    dict_box_left = dict_box['box_left']
    dict_box_right = dict_box['box_right']
    dict_skill_circle = config['SkillCircle']
    dict_skill_layout = config['SkillLayout']
    layout = Layout(dict_layout)
    box_top = Box(height=dict_box_top['size'], width=layout.width, color=dict_box_top['color'])
    box_bottom = Box(height=dict_box_bottom['size'], width=layout.width, color=dict_box_bottom['color'])
    box_left = Box(height=layout.height, width=dict_box_left['size'], color=dict_box_left['color'])
    box_right = Box(height=layout.height, width=dict_box_right['size'], color=dict_box_right['color'])
    skill_circle = SkillCircle(dict_skill_circle)
    skill_layout = SkillLayout(dict_skill_layout)
    return (layout, box_top, box_bottom, box_left, box_right, skill_circle, skill_layout)


