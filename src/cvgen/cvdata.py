#!/usr/bin/env python3

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
    def __init__(self, street, house, city, zipcode, country, phone, email, webpage, linkedin, xing, orcid, github):
        self.street = street
        self.house = house
        self.city = city
        self.zipcode = zipcode
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

