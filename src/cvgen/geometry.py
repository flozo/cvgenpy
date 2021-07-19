#!/usr/bin/env python3

import json


class Sepline:
    def __init__(self, sepline):
        self.x = sepline['x']
        self.y = sepline['y']
        self.width = sepline['width']
        self.thickness = sepline['thickness']
        self.color = sepline['color']


class Page:
    """
    General page properties
    """
    def __init__(self, settings):
        self.width = settings['width']
        self.height = settings['height']
        self.border_top = settings['border_top']
        self.border_bottom = settings['border_bottom']
        self.border_left = settings['border_left']
        self.border_right = settings['border_right']
        self.text_width = self.width-self.border_left-self.border_right
        self.text_height = self.height-self.border_top-self.border_bottom
        self.background_color = settings['background_color']
        self.draft = settings['draft']
        self.draft_highlight_color = settings['draft_highlight_color']

    def add_headsepline(self, thickness, color, fullwidth):
        """
        Add header separation line
        """
        args = {'x': self.border_left,
                'y': self.height-self.border_top,
                'width': self.text_width,
                'thickness': thickness,
                'color': color}
        if fullwidth is True:
            args['x'] = 0
            args['width'] = self.width
        sepline = Sepline(args)
        return '\\draw [draw={}, line width={}cm] ({}, {}) -- +({}, 0);'.format(sepline.color, sepline.thickness, sepline.x, sepline.y, sepline.width)

    def add_footsepline(self, thickness, color, fullwidth):
        """
        Add footer separation line
        """
        args = {'x': self.border_left,
                'y': self.border_bottom,
                'width': self.text_width,
                'thickness': thickness,
                'color': color}
        if fullwidth is True:
            args['x'] = 0
            args['width'] = self.width
        sepline = Sepline(args)
        return '\\draw [draw={}, line width={}cm] ({}, {}) -- +({}, 0);'.format(sepline.color, sepline.thickness, sepline.x, sepline.y, sepline.width)
 
    def add_title(self, text, fontsize, align, color, yshift):
        """
        Add page title
        """
        return '\\node [anchor=south west, text width={}cm, align={}, font=\\{}, color={}, yshift={}cm] at ({}, {}) {{{}}};'.format(self.text_width, align, fontsize, color, yshift, self.border_left, self.height-self.border_top, text)


class Layout(Page):
    """
    Specific CV properties
    """
    def __init__(self, layout):
        super().__init__(layout)
        self.pages = layout['pages']
        self.box_top = layout['box_top']
        self.box_bottom = layout['box_bottom']
        self.box_left = layout['box_left']
        self.box_right = layout['box_right']
        self.include_photo = layout['include_photo']
        self.title_on_every_page = layout['title_on_every_page']


class Letter(Page):
    """
    Specific letter properties
    """
    def __init__(self, letter):
        super().__init__(letter)
        self.address_x = letter['address_x']
        self.address_y = letter['address_y']
        self.address_width = letter['address_width']
        self.address_height = letter['address_height']
        self.backaddress_y = letter['backaddress_y']
        self.backaddress_sepline_thickness = letter['backaddress_sepline_thickness']
        self.backaddress_sepchar = letter['backaddress_sepchar']
        self.backaddress_fontsize = letter['backaddress_fontsize']
        self.sender_x = letter['sender_x']
        self.sender_y = letter['sender_y']
        self.sender_width = letter['sender_width']
        self.sender_height = letter['sender_height']
        self.subject_y = letter['subject_y']
        self.text_y = letter['text_y']
        self.closing_y_shift = letter['closing_y_shift']
        self.enclosure_y_shift = letter['enclosure_y_shift']
        self.perforation_mark_x = letter['perforation_mark_x']
        self.perforation_mark_y = letter['perforation_mark_y']
        self.perforation_mark_width = letter['perforation_mark_width']
        self.perforation_mark_thickness = letter['perforation_mark_thickness']
        self.folding_mark_1_x = letter['folding_mark_1_x']
        self.folding_mark_1_y = letter['folding_mark_1_y']
        self.folding_mark_1_width = letter['folding_mark_1_width']
        self.folding_mark_1_thickness = letter['folding_mark_1_thickness']
        self.folding_mark_2_x = letter['folding_mark_2_x']
        self.folding_mark_2_y = letter['folding_mark_2_y']
        self.folding_mark_2_width = letter['folding_mark_2_width']
        self.folding_mark_2_thickness = letter['folding_mark_2_thickness']
        

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


class Backaddress(object):
    def __init__(self, dict_pers, dict_address):
        self.first_name = dict_pers['first_name']
        self.family_name = dict_pers['family_name']
        self.street = dict_address['street']
        self.house = dict_address['house']
        self.postal_code = dict_address['postal_code']
        self.city = dict_address['city']
        self.country = dict_address['country']

    def oneline(self, space='1.5cm', separator='$\\bullet$'):
        return '{0} {1}\\hspace{{{6}}}{7}\\hspace{{{6}}}{2} {3}\\hspace{{{6}}}{7}\\hspace{{{6}}}{4} {5}'.format(self.first_name, self.family_name, self.street, self.house, self.postal_code, self.city, space, separator)


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
            'general': {
                'date_format': '%d.%m.%Y',
                },
            'structure': {
                'title_page': False,
                'letter': True,
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
                'border_top': 2.0,
                'border_bottom': 2.0,
                'border_left': 2.5,
                'border_right': 2.0,
                'language': 'en',
                'address_x': 2.0,
                'address_y': 20.7,
                'address_width': 9.0,
                'address_height': 4.5,
                'backaddress_y': 23.43,
                'backaddress_sepline_thickness': 0.5,
                'backaddress_sepchar': 'bullet',
                'backaddress_fontsize': 'scriptsize',
                'sender_x': 11.0,
                'sender_y': 20.7,
                'sender_width': 20.7,
                'sender_height': 20.7,
                'subject_y': 18.5,
                'text_y': 18.0,
                'closing_y_shift': 0.0,
                'enclosure_y_shift': -1.0,
                'perforation_mark_x': 0.1,
                'perforation_mark_y': 14.85,
                'perforation_mark_width': 0.5,
                'perforation_mark_thickness': 0.3,
                'folding_mark_1_x': 0.1,
                'folding_mark_1_y': 19.2,
                'folding_mark_1_width': 0.25,
                'folding_mark_1_thickness': 0.3,
                'folding_mark_2_x': 0.1,
                'folding_mark_2_y': 8.7,
                'folding_mark_2_width': 0.25,
                'folding_mark_2_thickness': 0.3,
                'background_color': 'none',
                'draft': False,
                'draft_highlight_color': 'Greys-D',
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
                    'border_top': 2.0,
                    'border_bottom': 2.0,
                    'border_left': 2.5,
                    'border_right': 2.0,
                    'pages': 1,
                    'background_color': 'none',
                    'box_top': False,
                    'box_bottom': False,
                    'box_left': True,
                    'box_right': False,
                    'include_photo': True,
                    'title_on_every_page': False,
                    'table_style': True,
                    'language': 'en',
                    'draft': False,
                    'draft_highlight_color': 'Greys-D',
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
                        'show_circles': False,
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

