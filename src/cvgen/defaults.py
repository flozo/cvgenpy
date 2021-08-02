#!/usr/bin/env python3

import json


def personal_data_config():
    """
    Create config file with generic settings.
    Settings are defined as nested dictionary and parsed to a JSON file.
    """
    settings_dict = {
            'Personal': {
                'first_name': 'John',
                'second_name': 'Peter',
                'family_name': 'Smith',
                'title': 'Ph.D.',
                'birth_date': '1900-01-01',
                'birth_location_city': 'City',
                'birth_location_country': 'Country',
                'citizenship': 'klingon',
                'marital_status': 'unmarried',
                'children': 'no',
                'photo': '/home/user/photo.jpg',
                'signature': '/home/user/signature.pdf',
                },
            'Contact': {
                'street': 'Street name',
                'house': '123a',
                'postal_code': '12345',
                'city': 'City',
                'country': 'Country',
                'phone': '+00(123)456789',
                'mobile': '+00(123)456789',
                'email': 'user@mail.net',
                'weblinks': {
                    'Webpage': 'https://www.webpage.net',
                    'LinkedIn': 'https://www.linkedin.com/in/john-smith-123456789/',
                    'Xing': 'https://www.xing.com/profile/john_smith123/',
                    'ORCID': 'https://orcid.org/0000-0000-1234-5678',
                    'GitHub': 'https://github.com/user',
                     },
                'icons': {
                    'address': 'address',
                    'phone': 'phone',
                    'email': 'mail',
                    'GitHub': 'github',
                    'LinkedIn': 'linkedin',
                    'ORCID': 'orcid',
                    },
               },
            'skills': {
                'skill1': {
                    'category': 'Programming',
                    'elements': 'Python, C++, Java',
                    },
                'skill2': {
                    'category': 'Operating systems',
                    'elements': 'GNU/Linux, Windows',
                    },
                },
            'knowledge': {
                    'item1': {
                        'name': 'English',
                        'description': 'native speaker',
                        'group': 'Languages',
                        },
                    'item2': {
                        'name': 'German',
                        'description': 'fluent',
                        'group': 'Languages',
                        },
                    'item3': {
                        'name': 'Latin',
                        'description': 'basic',
                        'group': 'Languages',
                        },
                    'item4': {
                        'name': 'Driving license',
                        'description': '',
                        'group': 'Licenses',
                        },
                    'item5': {
                        'name': 'Boating license',
                        'description': '',
                        'group': 'Licenses',
                        },
                    },
            'certificates': {
                    'item1': {
                        'name': 'MOOC certificate1',
                        'url': 'https://www.linktocertificate1.net',
                        'group': 'MOOC courses',
                        },
                    'item2': {
                        'name': 'MOOC certificate2',
                        'url': 'https://www.linktocertificate2.net',
                        'group': 'MOOC courses',
                        },
                    'item3': {
                        'name': 'MOOC certificate3',
                        'url': 'https://www.linktocertificate3.net',
                        'group': 'MOOC courses',
                        },
                    },
            'Education': {
                'period1': {
                    'start_date': '01/1990',
                    'end_date': '12/1997',
                    'school_name': 'School name1',
                    'school_type': 'High school',
                    'location': 'City',
                    'role': 'Student',
                    'description': 'What I did...',
                   },
                'event1': {
                    'date': '12/1997',
                    'school_name': 'School name1',
                    'school_type': 'High school',
                    'location': 'City',
                    'graduation': 'High-school diploma',
                    'grade': '1.2',
                    'thesis_title': '',
                    'role': 'Student',
                    'description': 'What I did...',
                   },
                'period2': {
                    'start_date': '01/1998',
                    'end_date': '12/2003',
                    'school_name': 'University of City',
                    'school_type': 'University',
                    'location': 'City',
                    'role': 'Master student',
                    'description': 'Master studies',
                    },
                'event2': {
                    'date': '12/2003',
                    'school_name': 'University of City',
                    'school_type': 'University',
                    'location': 'City',
                    'graduation': 'Master',
                    'grade': '1.2',
                    'thesis_title': 'Investigation of things by means of methods',
                    'role': 'Master student',
                    'description': '',
                    },
                'period3': {
                    'start_date': '01/2004',
                    'end_date': '12/2009',
                    'school_name': 'University of City',
                    'school_type': 'University',
                    'location': 'City',
                    'role': 'PhD student',
                    'description': 'Research, lab work, facility maintenance, teaching, student supervision',
                    },
                'event3': {
                    'date': '12/2009',
                    'school_name': 'University of City',
                    'school_type': 'University',
                    'location': 'City',
                    'graduation': 'PhD',
                    'grade': '1.2',
                    'thesis_title': 'Investigation of things by means of advanced methods',
                    'role': 'PhD student',
                    'description': '',
                    },
                },
            'Career': {
                    'Item1': {
                        'start_date': '01/2010',
                        'end_date': '12/2012',
                        'company_name': 'Company1',
                        'company_type': 'Biotech',
                        'location': 'City',
                        'role': 'Programmer',
                        'description': 'Backend development',
                        },
                    'Item2': {
                        'start_date': '01/2013',
                        'end_date': '12/2018',
                        'company_name': 'Company2',
                        'company_type': 'Finance',
                        'location': 'City',
                        'role': 'Data scientist',
                        'description': 'Dashboard design and data visualization',
                       },
                    'Item3': {
                        'start_date': '01/2019',
                        'end_date': '07/2021',
                        'company_name': 'Company3',
                        'company_type': 'Government agency',
                        'location': 'City',
                        'role': 'Data scientist',
                        'description': 'Public health data analysis',
                       },
                    },
            'enclosure': {
                    'Zeugnis': '',
                    'Promotionsurkunde': '',
                    'Diplom': '',
                    },
            }
    return settings_dict


def generic_company():
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
            "tag_number": "Tag no. 12345-67890",
            "salary_expectation": "1,000,000 EUR",
            "earliest_join_date": "1st of September",
            "color_main": "blue",
            "color_accent": "yellow",
            }
    return company_data


def write_letter(config_dir):
    """
    Create generic letter text with lorem ipsum.
    """
    text = """### Write your letter text below this #-commented header.
###
### You can include variables using braces {variable_name}.
###
### The following variables are available:
### {company}, {position}, {tag_number}, {salary_expectation}, {earliest_join_date}
###
### Letter text:
Dear Sir or Madam,

Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.

Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi.
"""
    with open(config_dir, 'w') as f:
        f.write(text)


def geometry_config():
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
                'closing_y_shift': 5.0,
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
                    'pages': 2,
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
                        'pos_x': 6.25,
                        'pos_y': 27,
                        'anchor': 'north west',
                        'head_vspace': 0.3,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'head_font_size': 'large',
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'normalsize',
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
                        'pos_y': 27,
                        'anchor': 'north west',
                        'width': 4.0,
                        'height': 6.0,
                        'border': True,
                        'border_width': 0.5,
                        'border_color': 'Greys-L',
                        },
                    'contact': {
                        'title': 'Contact',
                        'pos_x': 5.15,
                        'pos_y': 24,
                        'anchor': 'north west',
                        'head_vspace': 0.5,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'head_font_size': 'large',
                        'body_vspace': 1,
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'normalsize',
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
                        'pos_x': 2.2,
                        'pos_y': 18,
                        'anchor': 'north west',
                        'head_vspace': 0.5,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'head_font_size': 'large',
                        'body_vspace': 1,
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'normalsize',
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
                        'pos_x': 2.2,
                        'pos_y': 10,
                        'anchor': 'north west',
                        'head_vspace': 0.5,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'head_font_size': 'large',
                        'body_vspace': 1,
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'normalsize',
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
                        'pos_x': 2.2,
                        'pos_y': 22.5,
                        'anchor': 'north west',
                        'head_vspace': 0.5,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'head_font_size': 'large',
                        'body_vspace': 1,
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'normalsize',
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
                        'pos_x': 2.2,
                        'pos_y': 15.8,
                        'anchor': 'north west',
                        'head_vspace': 0.5,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'head_font_size': 'large',
                        'body_vspace': 1,
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'normalsize',
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
                        'pos_x': 6.0,
                        'pos_y': 9.7,
                        'anchor': 'north west',
                        'head_vspace': 0.5,
                        'head_sepline': False,
                        'head_case': 'upper',
                        'head_font_size': 'large',
                        'body_vspace': 1,
                        'body_vspace': 1,
                        'body_indent': 2,
                        'body_font_size': 'normalsize',
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
                        'size': 6.0,
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
    return settings_dict


def generic_enclosure():
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
    return settings_dict


def generic_preamble():
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
    return preamble


def generic_cell_styles():
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
    return cell_styles


def generic_layers():
    """
    Define generic TikZ layers. Default layer "main" has position 0.
    """
    layers_dict = {
            'layer1': {
                'name': 'background',
                'position': -2,
                },
            'layer2': {
                'name': 'forebackground',
                'position': -1,
                },
            'layer3': {
                'name': 'foreground',
                'position': 1,
                },
            }
    return layers_dict

