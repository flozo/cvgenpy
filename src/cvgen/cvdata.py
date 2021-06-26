#!/usr/bin/env python3

import json

class Personal(object):
    def __init__(self, dict_personal):
        self.first_name = dict_personal['first_name']
        self.second_name = dict_personal['second_name']
        self.family_name = dict_personal['family_name']
        self.birth_date = dict_personal['birth_date']
        self.birth_location_city = dict_personal['birth_location_city']
        self.birth_location_country = dict_personal['birth_location_country']
        self.married = dict_personal['married']
        self.children = dict_personal['children']


class Contact(object):
    def __init__(self, dict_contact):
        self.street = dict_contact['street']
        self.house = dict_contact['house']
        self.city = dict_contact['city']
        self.postalcode = dict_contact['postal_code']
        self.country = dict_contact['country']
        self.phone = dict_contact['phone']
        self.email = dict_contact['email']
        self.webpage = dict_contact['webpage']
        self.linkedin = dict_contact['linkedin']
        self.xing = dict_contact['xing']
        self.orcid = dict_contact['orcid']
        self.github = dict_contact['github']


class Company(object):
    def __init__(self, dict_company):
        self.name = dict_company['name']
        self.city = dict_company['city']
        self.color_main = dict_company['color_main']
        self.color_accent = dict_company['color_accent']


class SkillItem(object):
    def __init__(self, name, level):
        self.name = name
        self.level = level


class SkillGroup(object):
    def __init__(self, name, skill_items):
        self.name = name
        self.items = skill_items


def write_config(config_dir):
    """
    Create config file with generic settings.
    Settings are defined as nested dictionary and parsed to a JSON file.
    """
    settings_dict = {
            'Personal': {
                'first_name': 'John',
                'second_name': 'Peter',
                'family_name': 'Smith',
                'birth_date': '1900-01-01',
                'birth_location_city': 'City',
                'birth_location_country': 'Country',
                'married': False,
                'children': 0,
                },
            'Contact': {
                'street': 'Street name',
                'house': '123a',
                'city': 'City',
                'postal_code': '12345',
                'country': 'Country',
                'phone': '+00(123)456789',
                'email': 'user@mail.net',
                'webpage': 'https://www.webpage.net',
                'linkedin': 'https://www.linkedin.com/in/john-smith-123456789/',
                'xing': 'https://www.xing.com/profile/john_smith123/',
                'orcid': 'https://orcid.org/0000-0000-1234-5678',
                'github': 'https://github.com/user',
                },
            'Company': {
                'name': 'Company',
                'city': 'City',
                'color_main': 'blue',
                'color_accent': 'yellow',
                },
            'Skills': {
                'Skill1': {
                    'name': 'Skill1 name',
                    'level': 'Skill1 level',
                    'group': 'Skill1 group',
                    },
                'Skill2': {
                    'name': 'Skill2 name',
                    'level': 'Skill2 level',
                    'group': 'Skill2 group',
                    },
                'Skill3': {
                    'name': 'Skill3 name',
                    'level': 'Skill3 level',
                    'group': 'Skill3 group',
                    },
                },
            'Education': {
                'Item1': {
                    'caption': 'School1',
                    'location': 'City',
                    'description': 'What I did...',
                    'graduation': 'PhD',
                    'grade': '1.2',
                    'from': '01/1990',
                    'to': '12/1998',
                    },
                'Item2': {
                    'caption': 'School2',
                    'location': 'City',
                    'description': 'What I did...',
                    'from': '01/1990',
                    'to': '12/1998',
                    },
                },
            'Career': {
                    'Item1': {
                        'caption': 'Job1',
                        'location': 'City',
                        'description': 'What I did...',
                        'from': '01/1990',
                        'to': '12/1998',
                        },
                    'Item1': {
                        'caption': 'Job2',
                        'location': 'City',
                        'description': 'What I did...',
                        'from': '01/1990',
                        'to': '12/1998',
                        },
                    },
            }               
    with open(config_dir, 'w') as f:
        json.dump(settings_dict, f, indent=4)


def split_config(config):
    """
    Split dictionary from JSON config file into sub dictionaries.
    """
    dict_personal = config['Personal']
    dict_contact = config['Contact']
    dict_company = config['Company']
    dict_skills = config['Skills']
    person = Personal(dict_personal)
    contact = Contact(dict_contact)
    company = Company(dict_company)
    return (person, contact, company)

