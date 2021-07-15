#!/usr/bin/env python3

import json

class Personal(object):
    def __init__(self, dict_personal):
        self.first_name = dict_personal['first_name']
        self.second_name = dict_personal['second_name']
        self.family_name = dict_personal['family_name']
        self.title = dict_personal['title']
        self.birth_date = dict_personal['birth_date']
        self.birth_location_city = dict_personal['birth_location_city']
        self.birth_location_country = dict_personal['birth_location_country']
        self.marital_status = dict_personal['marital_status']
        self.children = dict_personal['children']
        self.photo = dict_personal['photo']
        self.signature = dict_personal['signature']


class Contact(object):
    def __init__(self, dict_contact):
        self.street = dict_contact['street']
        self.house = dict_contact['house']
        self.city = dict_contact['city']
        self.postalcode = dict_contact['postal_code']
        self.country = dict_contact['country']
        self.phone = dict_contact['phone']
        self.email = dict_contact['email']
        self.weblinks = dict_contact['weblinks']
        self.icons = dict_contact['icons']


class Company(object):
    def __init__(self, dict_company):
        self.name = dict_company['name']
        self.attention = dict_company['attention']
        self.street = dict_company['street']
        self.house = dict_company['house']
        self.city = dict_company['city']
        self.postalcode = dict_company['postalcode']
        self.position = dict_company['position']
        self.color_main = dict_company['color_main']
        self.color_accent = dict_company['color_accent']

    def address(self):
        if self.attention == '':
            return '{}\\\\{} {}\\\\{} {}'.format(self.name, self.street, self.house, self.postalcode, self.city)
        else:
            return '{}\\\\{}\\\\{} {}\\\\{} {}'.format(self.name, self.attention, self.street, self.house, self.postalcode, self.city)


class Metadata(object):
    def __init__(self, first_name, family_name, title, city, country, email, company, position, version):
        self.first_name = first_name
        self.family_name = family_name
        self.title = title
        self.city = city
        self.country = country
        self.email = email
        self.company = company
        self.position = position
        self.version = version


class SkillItem(object):
    def __init__(self, dict_skill):
        self.name = dict_skill['name']
        self.description = dict_skill['description']
        self.level = dict_skill['level']
        self.group = dict_skill['group']


class SkillGroup(object):
    def __init__(self, name, skill_items):
        self.name = name
        self.items = skill_items


class KnowledgeItem(object):
    def __init__(self, dict_know):
        self.name = dict_know['name']
        self.description = dict_know['description']
        self.group = dict_know['group']


class CertificateItem(object):
    def __init__(self, dict_cert):
        self.name = dict_cert['name']
        self.url = dict_cert['url']
        self.group = dict_cert['group']


class TimelineItem(object):
    """
    Generic timeline item
    """
    def __init__(self, date, institution_name, institution_type, location, role, description):
        self.date = date
        self.institution_name = institution_name
        self.institution_type = institution_type
        self.location = location
        self.role = role
        self.description = description


class PeriodItem(TimelineItem):
    """
    Defines a timeline period by extending TimelineItem by start_date
    """
    def __init__(self, start_date, end_date, institution_name, institution_type, location, role, description):
        self.start_date
        super().__init__(end_date, institution_name, institution_type, location, role, description)


class EduPeriodItem(PeriodItem):
    def __init__(self, dict_edu):
        self.start_date = dict_edu['start_date']
        self.end_date = dict_edu['end_date']
        self.school_name = dict_edu['school_name']
        self.school_type = dict_edu['school_type']
        self.location = dict_edu['location']
        self.role = dict_edu['role']
        self.description = dict_edu['description']
        super().__init__(self.start_date, self.end_date, self.school_name, self.school_type, self.location, self.role, self.description)


class EduEventItem(TimelineItem):
    def __init__(self, dict_edu):
        self.date = dict_edu['date']
        self.school_name = dict_edu['school_name']
        self.school_type = dict_edu['school_type']
        self.location = dict_edu['location']
        self.graduation = dict_edu['graduation']
        self.grade = dict_edu['grade']
        self.thesis_title = dict_edu['thesis_title']
        self.role = None
        self.description = dict_edu['description']
        super().__init__(self.date, self.school_name, self.school_type, self.location, self.role, self.description)


class CareerItem(PeriodItem):
    def __init__(self, dict_career):
        self.start_date = dict_career['start_date']
        self.end_date = dict_career['end_date']
        self.company_name = dict_career['company_name']
        self.company_type = dict_career['company_type']
        self.location = dict_career['location']
        self.role = dict_career['role']
        self.description = dict_career['description']
        super().__init__(self.start_date, self.end_date, self.company_name, self.company_type, self.location, self.role, self.description)


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
                'title': 'Ph.D.',
                'birth_date': '1900-01-01',
                'birth_location_city': 'City',
                'birth_location_country': 'Country',
                'marital_status': 'unmarried',
                'children': 'no',
                'photo': '/home/user/Photo1.jpg',
                'signature': '/home/user/Signature.pdf',
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
            'company': {
                'name': 'Company',
                'attention': 'James Jones',
                'street': 'Street name',
                'house': '987b',
                'city': 'City',
                'postalcode': '67890',
                'position': 'Position',
                'color_main': 'blue',
                'color_accent': 'yellow',
                },
            'skills': {
                'skill1': {
                    'name': 'Python',
                    'description': '',
                    'level': 4,
                    'group': 'Programming',
                    },
                'skill2': {
                    'name': 'LaTeX',
                    'description': '',
                    'level': 5,
                    'group': 'Programming',
                    },
                'skill3': {
                    'name': 'Bash',
                    'description': '',
                    'level': 3,
                    'group': 'Programming',
                    },
                'skill4': {
                    'name': 'GNU/Linux',
                    'description': '',
                    'level': 4,
                    'group': 'Operating systems',
                    },
                'skill5': {
                    'name': 'Windows',
                    'description': '',
                    'level': 3,
                    'group': 'Operating systems',
                    },
                'skill6': {
                    'name': 'Data analysis',
                    'description': 'numpy, scipy, pandas',
                    'level': 4,
                    'group': 'Software & Tools',
                    },
                'skill7': {
                    'name': 'Data visualization',
                    'description': 'matplotlib, gnuplot, pgfplots, Origin',
                    'level': 4,
                    'group': 'Software & Tools',
                    },
                'skill8': {
                    'name': 'Git',
                    'description': '',
                    'level': 5,
                    'group': 'Software & Tools',
                    },
                'skill9': {
                    'name': 'MS Office/LibreOffice',
                    'description': '',
                    'level': 4,
                    'group': 'Software & Tools',
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


def write_letter(config_dir):
    """
    Create generic letter text with lorem ipsum.
    """
    text = """### Use {Company}, {Position}, {Name} to include variables:
###
### Letter text: 
Dear Sir or Madam,
               
Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
               
Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.
               
Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi.

"""
    with open(config_dir, 'w') as f:
        f.write(text)
#        json.dump(text, f, indent=4)

           
