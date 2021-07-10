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
        self.include_photo = dict_layout['include_photo']
        self.title_on_every_page = dict_layout['title_on_every_page']


class Address(object):
    def __init__(self, dict_address):
        self.street = dict_address['street']
        self.house = dict_address['house']
        self.postal_code = dict_address['postal_code']
        self.city = dict_address['city']
        self.country = dict_address['country']

    def oneline(self):
        return '{} {}, {} {}'.format(self.street, self.house, self.postal_code, self.city)

    def twoline(self):
        return '{} {}\\\\{} {}'.format(self.street, self.house, self.postal_code, self.city)


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

    def twoline(self, lang):
        if lang == 'en':
            about_str = 'Born {} in {}\\\\{}, {} children'.format(self.birth_date, self.birth_location_city, self.marital_status, self.children)
        if lang == 'de':
            about_str = 'Geboren am {} in {}\\\\{}, {} Kinder'.format(self.birth_date, self.birth_location_city, self.marital_status, self.children)
        return about_str


class PhotoArea(object):
    def __init__(self, dict_photo):
        self.pos_x = dict_photo['pos_x']
        self.pos_y = dict_photo['pos_y']
        self.anchor = dict_photo['anchor']
        self.width = dict_photo['width']
        self.height = dict_photo['height']
        self.border = dict_photo['border']
        self.border_width = dict_photo['border_width']
        self.border_color = dict_photo['border_color']


class Area(object):
    def __init__(self, dict_area):
        self.title = dict_area['title']
        self.pos_x = dict_area['pos_x']
        self.pos_y = dict_area['pos_y']
        self.anchor = dict_area['anchor']
        self.head_vspace = dict_area['head_vspace']
        self.head_sepline = dict_area['head_sepline']
        self.head_case = dict_area['head_case']
        self.head_font_size = dict_area['head_font_size']
        self.body_vspace = dict_area['body_vspace']
        self.body_indent = dict_area['body_indent']
        self.body_font_size = dict_area['body_font_size']
        self.color = dict_area['color']
        self.length = dict_area['length']
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
    def __init__(self, color, width, height):
        self.color = color
        self.width = width
        self.height = height


class SkillCircle(object):
    def __init__(self, dict_skill_circle):
        self.radius = dict_skill_circle['radius']
        self.fillcolor = dict_skill_circle['fillcolor']
        self.opencolor = dict_skill_circle['opencolor']
        self.linecolor = dict_skill_circle['linecolor']
        self.showline = dict_skill_circle['showline']


class SkillLayout(object):
    def __init__(self, dict_skill_layout):
        self.number = dict_skill_layout['circle_number']
        self.distance = dict_skill_layout['circle_distance']


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
                    'title_on_every_page': False,
                    'language': 'en',
                    },
                'areas': {
                    'title': {
                        'title': 'Curriculum vitae',
                        'pos_x': 8.0,
                        'pos_y': 29,
                        'anchor': 'north west',
                        'head_vspace': 0.3,
                        'head_sepline': True,
                        'head_case': 'mixed',
                        'head_font_size': 'LARGE',
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'large',
                        'color': 'black',
                        'icon_color': 'black',
                        'length': 20,
                        'style': 'oneline',
                        'icon': '/home/user/Icon1.pdf',
                        'show_area': True,
                        'show_icon': False,
                        'hyperlinks': False,
                        'hide_items': [],
                        },
                    'personal': {
                        'title': 'About me',
                        'pos_x': 8.0,
                        'pos_y': 26,
                        'anchor': 'north west',
                        'head_vspace': 0.3,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'head_font_size': 'large',
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'small',
                        'color': 'black',
                        'icon_color': 'black',
                        'length': 9.5,
                        'style': 'oneline',
                        'icon': '/home/user/Icon1.pdf',
                        'show_area': True,
                        'show_icon': False,
                        'hyperlinks': False,
                        'hide_items': [],
                        },
                    'photo': {
                        'pos_x': 16,
                        'pos_y': 28,
                        'anchor': 'north west',
                        'width': 4.0,
                        'height': 6.0,
                        'border': True,
                        'border_width': 0.5,
                        'border_color': 'Greys-L',
                        },
                    'contact': {
                        'title': 'Contact',
                        'pos_x': 0.6,
                        'pos_y': 26,
                        'anchor': 'north west',
                        'head_vspace': 0.5,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'head_font_size': 'large',
                        'body_vspace': 1,
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'footnotesize',
                        'color': 'black',
                        'icon_color': 'Blues-K',
                        'length': 10,
                        'style': 'table',
                        'icon': '/home/user/Icon2.pdf',
                        'show_area': True,
                        'show_icon': False,
                        'hyperlinks': True,
                        'hide_items': ['Webpage', 'Xing', 'phone', 'country', 'GitHub'],
                        },
                    'career': {
                        'title': 'Career',
                        'pos_x': 8.0,
                        'pos_y': 23,
                        'anchor': 'north west',
                        'head_vspace': 0.5,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'head_font_size': 'large',
                        'body_vspace': 1,
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'small',
                        'color': 'black',
                        'icon_color': 'black',
                        'length': 10,
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
                        'anchor': 'north west',
                        'head_vspace': 0.5,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'head_font_size': 'large',
                        'body_vspace': 1,
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'small',
                        'color': 'black',
                        'icon_color': 'black',
                        'length': 10,
                        'style': 'table',
                        'icon': '/home/user/Icon4.pdf',
                        'show_area': True,
                        'show_icon': False,
                        'hyperlinks': False,
                        'hide_items': [],
                        },
                    'skills': {
                        'title': 'Skill profile',
                        'pos_x': 0.6,
                        'pos_y': 20.5,
                        'anchor': 'north west',
                        'head_vspace': 0.5,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'head_font_size': 'large',
                        'body_vspace': 1,
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'footnotesize',
                        'color': 'black',
                        'icon_color': 'black',
                        'length': 10,
                        'style': 'table',
                        'icon': '/home/user/Icon5.pdf',
                        'show_area': True,
                        'show_icon': False,
                        'hyperlinks': False,
                        'hide_items': [],
                        },
                    'knowledge': {
                        'title': 'Knowledge',
                        'pos_x': 0.6,
                        'pos_y': 9.8,
                        'anchor': 'north west',
                        'head_vspace': 0.5,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'head_font_size': 'large',
                        'body_vspace': 1,
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'footnotesize',
                        'color': 'black',
                        'icon_color': 'black',
                        'length': 10,
                        'style': 'list',
                        'icon': '/home/user/Icon6.pdf',
                        'show_area': True,
                        'show_icon': False,
                        'hyperlinks': False,
                        'hide_items': [],
                        },
                    'certificates': {
                        'title': 'Certificates',
                        'pos_x': 0.6,
                        'pos_y': 3.7,
                        'anchor': 'north west',
                        'head_vspace': 0.5,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'head_font_size': 'large',
                        'body_vspace': 1,
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'footnotesize',
                        'color': 'black',
                        'icon_color': 'black',
                        'length': 10,
                        'style': 'list',
                        'icon': '/home/user/Icon6.pdf',
                        'show_area': True,
                        'show_icon': False,
                        'hyperlinks': True,
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
                        'circle_distance': 0.35,
                        'group_color': 'Blues-K',
                        },
                    'circle': {
                        'radius': 1.6,
                        'fillcolor': 'Blues-K',
                        'opencolor': 'Greys-G',
                        'linecolor': 'black',
                        'showline': False,
                        },
                   },
                },
            }
    with open(config_dir, 'w') as f:
        json.dump(settings_dict, f, indent=4)

