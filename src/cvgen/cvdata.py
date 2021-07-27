#!/usr/bin/env python3

from datetime import datetime


class Personal(object):
    def __init__(self, dict_personal):
        self.first_name = dict_personal['first_name']
        self.second_name = dict_personal['second_name']
        self.family_name = dict_personal['family_name']
        self.title = dict_personal['title']
        self.birth_date = dict_personal['birth_date']
        self.birth_location_city = dict_personal['birth_location_city']
        self.birth_location_country = dict_personal['birth_location_country']
        self.citizenship = dict_personal['citizenship']
        self.marital_status = dict_personal['marital_status']
        self.children = dict_personal['children']
        self.photo = dict_personal['photo']
        self.signature = dict_personal['signature']


class Address:
    def __init__(self, address):
        self.street = address['street']
        self.house = address['house']
        self.postalcode = address['postal_code']
        self.city = address['city']
        self.country = address['country']


class Contact(Address):
    def __init__(self, contact):
        super().__init__(contact)
        self.phone = contact['phone']
        self.email = contact['email']
        self.weblinks = contact['weblinks']
        self.icons = contact['icons']


class Company(Address):
    def __init__(self, company):
        super().__init__(company)
        self.name = company['name']
        self.attention = company['attention']
        self.position = company['position']
        self.tag_number = company['tag_number']
        self.salary_expectation = company['salary_expectation']
        self.earliest_join_date = company['earliest_join_date']
        self.color_main = company['color_main']
        self.color_accent = company['color_accent']

    def address(self):
        if self.attention == '':
            return '{}\\\\{} {}\\\\{} {}'.format(self.name, self.street, self.house, self.postalcode, self.city)
        else:
            return '{}\\\\{}\\\\{} {}\\\\{} {}'.format(self.name, self.attention, self.street, self.house, self.postalcode, self.city)


class Metadata(object):
    """
    Definition of PDF metadata.
    """
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

    def generate(self):
        """
        Generate LaTeX code with PDF metadata for hypersetup.
        """
        l = [
                '\t' + 'pdftitle={{Bewerbung bei {} als {}}},'.format(self.company, self.position),
                '\t' + r'pdfsubject={Bewerbung},',
                '\t' + 'pdfauthor={{{} {}}},'.format(self.first_name, self.family_name),
                '\t' + 'pdfauthortitle={{{}}},'.format(self.title),
                '\t' + 'pdfcaptionwriter={{{} {}}},'.format(self.first_name, self.family_name),
                '\t' + 'pdfdate={{{}}},'.format(datetime.today().strftime('%Y-%m-%d')),
                '\t' + 'pdfproducer={{cvgen {} by flozo}},'.format(self.version),
                '\t' + 'pdfcontactcity={{{}}},'.format(self.city),
                '\t' + 'pdfcontactcountry={{{}}},'.format(self.country),
                '\t' + 'pdfcontactemail={{{}}},'.format(self.email),
                ]
        return l


class SkillItem(object):
    def __init__(self, category, elements):
        self.category = category
        self.elements = elements
#        self.name = dict_skill['name']
#        self.description = dict_skill['description']
#        self.level = dict_skill['level']
#        self.group = dict_skill['group']


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

