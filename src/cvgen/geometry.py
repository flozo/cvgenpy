#!/usr/bin/env python3

import json


class Layout(object):
    def __init__(self, dict_layout):
        self.width = dict_layout['width']
        self.height = dict_layout['height']
        self.pages = dict_layout['pages']
        self.background_color = dict_layout['background_color']
        self.box_top = dict_layout['box_top']
        self.box_bottom = dict_layout['box_bottom']
        self.box_left = dict_layout['box_left']
        self.box_right = dict_layout['box_right']
#        super().__init__(size, color)


class Area(object):
    def __init__(self, dict_area):
#    def __init__(self, title, pos_x, pos_y, color, icon, show_area, show_icon):
        self.title = dict_area['title']
        self.pos_x = dict_area['pos_x']
        self.pos_y = dict_area['pos_y']
        self.head_vspace = dict_area['head_vspace']
        self.head_sepline = dict_area['head_sepline']
        self.head_case = dict_area['head_case']
        self.body_vspace = dict_area['body_vspace']
        self.color = dict_area['color']
        self.style = dict_area['style']
        self.icon = dict_area['icon']
        self.show_area = dict_area['show_area']
        self.show_icon = dict_area['show_icon']
        if self.head_case == 'upper':
            self.title = self.title.upper()
        elif self.head_case == 'lower':
            self.title = self.title.lower()


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
        self.opencolor = dict_skill_circle['opencolor']
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
                'language': 'en',
                },
            'letter': {
                'width': 21.0,
                'height': 29.7,
                'language': 'en',
                },
            'cv': {
                'layout': {
                    'width': 21.0,
                    'height': 29.7,
                    'pages': 2,
                    'background_color': 'white',
                    'box_top': False,
                    'box_bottom': False,
                    'box_left': True,
                    'box_right': False,
                    'include_photo': True,
                    'language': 'en',
                    },
                'areas': {
                    'personal': {
                        'title': 'About me',
                        'pos_x': 8,
                        'pos_y': 25,
                        'head_vspace': 0.3,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'body_vspace': 1,
                        'color': 'black',
                        'style': 'oneline',
                        'icon': '/home/user/Icon1.pdf',
                        'show_area': True,
                        'show_icon': False,
                        },
                    'contact': {
                        'title': 'Contact',
                        'pos_x': 2,
                        'pos_y': 25,
                        'head_vspace': 1,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'body_vspace': 1,
                        'color': 'black',
                        'style': 'table',
                        'icon': '/home/user/Icon2.pdf',
                        'show_area': True,
                        'show_icon': False,
                        },
                    'timeline': {
                        'title': 'Career',
                        'pos_x': 10,
                        'pos_y': 20,
                        'head_vspace': 1,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'body_vspace': 1,
                        'color': 'black',
                        'style': 'table',
                        'icon': '/home/user/Icon3.pdf',
                        'show_area': True,
                        'show_icon': False,
                        },
                    'timeline': {
                        'title': 'Education',
                        'pos_x': 10,
                        'pos_y': 15,
                        'head_vspace': 1,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'body_vspace': 1,
                        'color': 'black',
                        'style': 'table',
                        'icon': '/home/user/Icon4.pdf',
                        'show_area': True,
                        'show_icon': False,
                        },
                    'skills': {
                        'title': 'Skill profile',
                        'pos_x': 2,
                        'pos_y': 10,
                        'head_vspace': 1,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'body_vspace': 1,
                        'color': 'black',
                        'style': 'table',
                        'icon': '/home/user/Icon5.pdf',
                        'show_area': True,
                        'show_icon': False,
                        },
                    'knowledge': {
                        'title': 'Certificates',
                        'pos_x': 2,
                        'pos_y': 5,
                        'head_vspace': 1,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'body_vspace': 1,
                        'color': 'black',
                        'style': 'list',
                        'icon': '/home/user/Icon6.pdf',
                        'show_area': True,
                        'show_icon': False,
                        },
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
                        'size': 7,
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
                        'opencolor': 'Reds-D',
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

