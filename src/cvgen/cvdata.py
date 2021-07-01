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
        self.marital_status = dict_personal['marital_status']
        self.children = dict_personal['children']
        self.photo = dict_personal['photo']


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


class TimelineItem(object):
    """
    Generic timeline item
    """
    def __init__(self, date, institution_name, institution_type, location, description):
        self.date = date
        self.institution_name = institution_name
        self.institution_type = institution_type
        self.location = location
        self.description = description


class PeriodItem(TimelineItem):
    """
    Defines a timeline period by extending TimelineItem by start_date
    """
    def __init__(self, start_date, end_date, institution_name, institution_type, location, description):
        self.start_date
        super().__init__(end_date, institution_name, institution_type, location, description)


class EduPeriodItem(PeriodItem):
    def __init__(self, dict_edu_item):
        self.start_date = dict_edu_item['start_date']
        self.end_date = dict_edu_item['end_date']
        self.school_name = dict_edu_item['school_name']
        self.school_type = dict_edu_item['school_type']
        self.location = dict_edu_item['location']
        self.description = dict_edu_item['description']
        super().__init__(self.start_date, self.end_date, self.school_name, self.school_type, self.location, self.description)


class EduEventItem(TimelineItem):
    def __init__(self, dict_edu_item):
        self.date = dict_edu_item['date']
        self.school_name = dict_edu_item['school_name']
        self.school_type = dict_edu_item['school_type']
        self.location = dict_edu_item['location']
        self.graduation = dict_edu_item['graduation']
        self.grade = dict_edu_item['grade']
        self.thesis_title = dict_edu_item['thesis_title']
        self.description = dict_edu_item['description']
        super().__init__(self.date, self.school_name, self.school_type, self.location, self.description)


class CareerItem(object):
    def __init(self, caption, company, location, description, beginning, end):
        self.caption = caption
        self.company = company
        self.location = location
        self.description = description
        self.beginning = beginning
        self.end = end


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
                'marital_status': 'unmarried',
                'children': 'no',
                'photo': '/home/user/Photo1.jpg',
                },
            'Contact': {
                'street': 'Street name',
                'house': '123a',
                'city': 'City',
                'postal_code': '12345',
                'country': 'Country',
                'phone': '+00(123)456789',
                'mobile': '+00(123)456789',
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
                'period1': {
                    'start_date': '01/1990',
                    'end_date': '12/1997',
                    'school_name': 'School name1',
                    'school_type': 'High school',
                    'location': 'City',
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
                    'description': 'What I did...',
                   },
                'period2': {
                    'start_date': '01/1998',
                    'end_date': '12/2003',
                    'school_name': 'University of City',
                    'school_type': 'University',
                    'location': 'City',
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
                    'description': '',
                    },
                'period3': {
                    'start_date': '01/2004',
                    'end_date': '12/2009',
                    'school_name': 'University of City',
                    'school_type': 'University',
                    'location': 'City',
                    'description': 'PhD studies',
                    },
                'event3': {
                    'date': '12/2009',
                    'school_name': 'University of City',
                    'school_type': 'University',
                    'location': 'City',
                    'graduation': 'PhD',
                    'grade': '1.2',
                    'thesis_title': 'Investigation of things by means of advanced methods',
                    'description': '',
                    },
                },
            'Career': {
                    'Item1': {
                        'caption': 'Job1',
                        'company': 'Company1',
                        'location': 'City',
                        'description': 'What I did...',
                        'start_date': '01/2010',
                        'end_date': '12/2011',
                        },
                    'Item2': {
                        'caption': 'Job2',
                        'company': 'Company2',
                        'location': 'City',
                        'description': 'What I did...',
                        'start_date': '01/2012',
                        'end_date': '12/2018',
                        },
                    'Item3': {
                        'caption': 'Job3',
                        'company': 'Company3',
                        'location': 'City',
                        'description': 'What I did...',
                        'start_date': '01/2019',
                        'end_date': '06/2021',
                        },
                    },
            'Appendix': {
                    'Appendix1': {
                        'name': 'Reference letter1',
                        'file': '/home/user/Reference_letter1.pdf',
                        },
                    'Appendix2': {
                        'name': 'Reference letter2',
                        'file': '/home/user/Reference_letter2.pdf',
                        },
                    'Appendix3': {
                        'name': 'School certificate',
                        'file': '/home/user/School_certificate.pdf',
                        },
                    'Appendix4': {
                        'name': 'Bachelor certificate',
                        'file': '/home/user/Bachelor_certificate.pdf',
                        },
                    'Appendix5': {
                        'name': 'Master certificate',
                       'file': '/home/user/Master_certificate.pdf',
                        },
                    'Appendix6': {
                        'name': 'PhD certificate',
                        'file': '/home/user/PhD_certificate.pdf',
                        },
                    'Appendix7': {
                        'name': 'MOOC certificate1',
                        'file': '/home/user/MOOC_certificate1.pdf',
                        },
                    'Appendix8': {
                        'name': 'MOOC certificate2',
                        'file': '/home/user/MOOC_certificate2.pdf',
                        },
                    },
            }               
    with open(config_dir, 'w') as f:
        json.dump(settings_dict, f, indent=4)

