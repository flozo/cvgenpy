#!/usr/bin/env python3

import json

class Personal(object):
    def __init__(self, first_name, second_name, hide_second_name, family_name, birth_date, birth_location, married, children):
        self.first_name = first_name
        self.second_name = second_name
        self.hide_second_name = hide_second_name
        self.family_name = family_name
        self.birth_date = birth_date
        self.birth_location = birth_location
        self.married = married
        self.children = children


class Contact(object):
    def __init__(self, street, house, city, postal_code, country, phone, email, webpage, linkedin, xing, orcid, github):
        self.street = street
        self.house = house
        self.city = city
        self.postalcode = postal_code
        self.country = country
        self.phone = phone
        self.email = email
        self.webpage = webpage
        self.linkedin = linkedin
        self.xing = xing
        self.orcid = orcid
        self.github = github


class Company(object):
    def __init__(self, name, city, color_main, color_accent):
        self.name = name
        self.city = city
        self.color_main = color_main
        self.color_accent = color_accent


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

