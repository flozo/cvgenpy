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


class Address(object):
    def __init__(self, dict_address):
        self.street = dict_address['street']
        self.house = dict_address['house']
        self.postal_code = dict_address['postal_code']
        self.city = dict_address['city']
        self.country = dict_address['country']

    def oneline(self):
        return '{} {}, {} {}'.format(self.street, self.house, self.postal_code, self.city)


class Personal(object):
    def __init__(self, dict_pers):
        self.birth_date = dict_pers['birth_date']
        self.birth_location_city = dict_pers['birth_location_city']
        self.marital_status = dict_pers['marital_status']
        self.children = dict_pers['children']

    def oneline(self, lang):
        if lang == 'en':
            about_str = 'Born {} in {}, {}, {} children'.format(self.birth_date, self.birth_location_city, self.marital_status, self.children)
        if lang == 'de':
            about_str = 'Geboren am {} in {}, {}, {} Kinder'.format(self.birth_date, self.birth_location_city, self.marital_status, self.children)
        return about_str


class PhotoArea(object):
    def __init__(self, dict_photo):
        self.pos_x = dict_photo['pos_x']
        self.pos_y = dict_photo['pos_y']
        self.width = dict_photo['width']
        self.height = dict_photo['height']
        self.border = dict_photo['border']
        self.border_width = dict_photo['border_width']
        self.border_color = dict_photo['border_color']


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
        self.body_indent = dict_area['body_indent']
        self.color = dict_area['color']
        self.style = dict_area['style']
        self.icon = dict_area['icon']
        self.show_area = dict_area['show_area']
        self.show_icon = dict_area['show_icon']
        self.hyperlinks = dict_area['hyperlinks']
        self.hide_items = dict_area['hide_items']
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
            'icons': {
                'address': r'\faIcon{map-marker-alt}',
                'phone': r'\faIcon{phone-alt}',
                'mail': r'\faIcon{envelope}',
                'github': r'\faIcon{github}',
                'xing': r'\faIcon{xing-square}',
                'linkedin': r'\faIcon{linkedin}',
                'orcid': r'\faIcon{orcid}',
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
                    'title': 'Curriculum vitae',
                    'title_on_every_page': False,
                    'language': 'en',
                    },
                'areas': {
                    'personal': {
                        'title': 'About me',
                        'pos_x': 8.0,
                        'pos_y': 26,
                        'head_vspace': 0.3,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'body_vspace': 1,
                        'body_indent': 2,
                        'color': 'black',
                        'style': 'oneline',
                        'icon': '/home/user/Icon1.pdf',
                        'show_area': True,
                        'show_icon': False,
                        'hyperlinks': False,
                        'hide_items': [],
                        },
                    'photo': {
                        'pos_x': 16.8,
                        'pos_y': 29,
                        'width': 3.2,
                        'height': 4.5,
                        'border': True,
                        'border_width': 0.1,
                        'border_color': 'Greys-L',
                        },
                    'contact': {
                        'title': 'Contact',
                        'pos_x': 0.8,
                        'pos_y': 26,
                        'head_vspace': 1,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'body_vspace': 1,
                        'body_indent': 2,
                        'color': 'black',
                        'style': 'table',
                        'icon': '/home/user/Icon2.pdf',
                        'show_area': True,
                        'show_icon': False,
                        'hyperlinks': True,
                        'hide_items': ['webpage', 'xing', 'phone', 'country'],
                        },
                    'career': {
                        'title': 'Career',
                        'pos_x': 8.0,
                        'pos_y': 23,
                        'head_vspace': 1,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'body_vspace': 1,
                        'body_indent': 2,
                        'color': 'black',
                        'style': 'table',
                        'icon': '/home/user/Icon3.pdf',
                        'show_area': True,
                        'show_icon': False,
                        'hyperlinks': False,
                        'hide_items': [],
                        },
                    'education': {
                        'title': 'Education',
                        'pos_x': 8.0,
                        'pos_y': 16,
                        'head_vspace': 1,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'body_vspace': 1,
                        'body_indent': 2,
                        'color': 'black',
                        'style': 'table',
                        'icon': '/home/user/Icon4.pdf',
                        'show_area': True,
                        'show_icon': False,
                        'hyperlinks': False,
                        'hide_items': [],
                        },
                    'skills': {
                        'title': 'Skill profile',
                        'pos_x': 2,
                        'pos_y': 12,
                        'head_vspace': 1,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'body_vspace': 1,
                        'body_indent': 2,
                        'color': 'black',
                        'style': 'table',
                        'icon': '/home/user/Icon5.pdf',
                        'show_area': True,
                        'show_icon': False,
                        'hyperlinks': False,
                        'hide_items': [],
                        },
                    'knowledge': {
                        'title': 'Certificates',
                        'pos_x': 2,
                        'pos_y': 5,
                        'head_vspace': 1,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'body_vspace': 1,
                        'body_indent': 2,
                        'color': 'black',
                        'style': 'list',
                        'icon': '/home/user/Icon6.pdf',
                        'show_area': True,
                        'show_icon': False,
                        'hyperlinks': False,
                        'hide_items': [],
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
                        'size': 7.5,
                        'color': 'Greys-C',
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
                        'circle_distance': 3.6,
                        },
                    'circle': {
                        'radius': 1.5,
                        'fillcolor': 'Blues-K',
                        'opencolor': 'Blues-D',
                        'linecolor': 'black',
                        'showline': False,
                        },
                   },
                },
            }
    with open(config_dir, 'w') as f:
        json.dump(settings_dict, f, indent=4)

