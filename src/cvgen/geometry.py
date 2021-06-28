#!/usr/bin/env python3

import json


class Layout(object):
    def __init__(self, dict_layout):
        self.width = dict_layout['width']
        self.height = dict_layout['height']
        self.background_color = dict_layout['background_color']
        self.box_top = dict_layout['box_top']
        self.box_bottom = dict_layout['box_bottom']
        self.box_left = dict_layout['box_left']
        self.box_right = dict_layout['box_right']
#        super().__init__(size, color)


class Box(object):
#    def __init__(self, dict_box):
    def __init__(self, color, width, height):
        self.color = color
        self.width = width
        self.height = height
#        self.size = dict_box['size']
#        self.color = dict_box['color']


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
        self.number = dict_skill_layout['circle_number']
        self.distance = dict_skill_layout['circle_distance']
#        super().__init__(radius=2, fillcolor, linecolor, showline=False)


def write_config(config_dir):
    """
    Create geometry config file with generic settings.
    Settings are defined as nested dictionary and parsed to a JSON file.
    """
    settings_dict = {
            'structure': {
                'title_page': False,
                'letter': False,
                'cv': True,
                'appendices': False,
                },
            'title': {
                'width': 21.0,
                'height': 29.7,
                'show_photo': False,
                'show_name': True,
                'show_address': True,
                'show_phone_number': True,
                'show_email_address': True,
                },
            'letter': {
                'width': 21.0,
                'height': 29.7,
                },
            'cv': {
                'layout': {
                    'width': 21.0,
                    'height': 29.7,
                    'background_color': 'white',
                    'box_top': False,
                    'box_bottom': False,
                    'box_left': True,
                    'box_right': False,
                    'include_photo': True,
                    },
                'boxes': {
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
                'skills': {
                    'layout': {
                        'show_circles': True,
                        'circle_number': 5,
                        'circle_distance': 5,
                        },
                    'circle': {
                        'radius': 2,
                        'fillcolor': 'Reds-E',
                        'linecolor': 'black',
                        'showline': False,
                        },
                   },
                },
            }
    with open(config_dir, 'w') as f:
        json.dump(settings_dict, f, indent=4)


def split_config(config):
    """
    Split dictionary from JSON config file into sub dictionaries.
    """
    dict_layout = config['cv']['layout']
    dict_box = config['cv']['boxes']
    dict_box_top = dict_box['box_top']
    dict_box_bottom = dict_box['box_bottom']
    dict_box_left = dict_box['box_left']
    dict_box_right = dict_box['box_right']
    dict_skill_layout = config['cv']['skills']['layout']
    dict_skill_circle = config['cv']['skills']['circle']
    layout = Layout(dict_layout)
    background_box = Box(color=dict_layout['background_color'], width=dict_layout['width'], height=dict_layout['height'])
    box_top = Box(color=dict_box_top['color'], width=layout.width, height=dict_box_top['size'])
    box_bottom = Box(color=dict_box_bottom['color'], width=layout.width, height=dict_box_bottom['size'])
    box_left = Box(color=dict_box_left['color'], width=dict_box_left['size'], height=layout.height)
    box_right = Box(color=dict_box_right['color'], width=dict_box_right['size'], height=layout.height)
    skill_circle = SkillCircle(dict_skill_circle)
    skill_layout = SkillLayout(dict_skill_layout)
    return (layout, box_top, box_bottom, box_left, box_right, skill_circle, skill_layout)

