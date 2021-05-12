class Box(object):
    def __init__(self, height, width, color):
        self.height = height
        self.width = width
        self.color = color


class Layout(Box):
    def __init__(self, height, width, color, box_top, box_bottom, box_left, box_right):
        self.box_top = box_top
        self.box_bottom = box_bottom
        self.box_left = box_left
        self.box_right = box_right
        super().__init__(height, width, color)

 
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

