#!/usr/bin/env python3

import json
from PyPDF2 import PdfFileReader


class Preamble:
    """
    Define LaTeX preamble
    """
    def __init__(self, documentclass, packages, settings, metadata):
       self.documentclass = documentclass
       self.packages = packages
       self.settings = settings
       self.metadata = metadata

    def generate(self):
        """
        Generate LaTeX code for preamble
        """
        # Generate code for documentclass
        dc = list(self.documentclass.items())[0]
        l = ['\\documentclass[{classoptions}]{{{classname}}}'.format(classoptions=dc[1], classname=dc[0])]
        # Generate code for packages
        for key, value in self.packages.items():
            if value != '':
                l.append('\\usepackage[{packageoptions}]{{{packagename}}}'.format(packageoptions=value, packagename=key))
            else:
                l.append('\\usepackage{{{packagename}}}'.format(packagename=key))
        # Generate code for package settings
        for key, value in self.settings.items():
            # Special treatment for hypersetup if metadata has to be included:
            if key == 'hypersetup' and self.metadata is not None:
                l = l + self.include_meta()
            else:
                l.append('\\{name}{{{arguments}}}'.format(name=key, arguments=value))
        return l

    def include_meta(self):
        """
        Include metadata to hypersetup in preamble
        """
        # Store non-meta data hypersetup settings in variable
        hypersetup = self.settings['hypersetup'].split(',')
        # Rewrite LaTeX code for hypersetup including meta and non-meta data
        l = ['\\hypersetup{']
        for item in hypersetup:
            l.append('\t' + item.replace(' ', '') + ',')
        l = l + self.metadata
        l.append('\t}')
        return l


class Sepline:
    """
    Define separation line.
    """
    def __init__(self, sepline):
        self.x = sepline['x']
        self.y = sepline['y']
        self.width = sepline['width']
        self.thickness = sepline['thickness']
        self.color = sepline['color']


class Page:
    """
    Define general page properties.
    """
    def __init__(self, name, settings):
        self.name = name
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
        self.language = settings['language']

    def add_headsepline(self, thickness, color, fullwidth):
        """
        Add header separation line.
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
        Add footer separation line.
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
        Add page title.
        """
        return '\\node [anchor=south west, text width={}cm, align={}, font=\\{}, color={}, yshift={}cm] at ({}, {}) {{{}}};'.format(self.text_width, align, fontsize, color, yshift, self.border_left, self.height-self.border_top, text)

    def latex_head(self):
        """
        LaTeX code for a tikzpicture head.
        """
        l = [
                '% {}'.format(self.name.upper()),
                '\\begin{tikzpicture}[',
                '\t' + 'inner xsep=0pt,',
                '\t' + 'inner ysep=0pt,',
                '\t' + 'trim left=0pt,',
                '\t' + 'trim right={\\paperw cm},',
                '\t' + ']',
                ]
        return l

    def latex_foot(self):
        """
        LaTeX code for a tikzpicture foot.
        """
        return ['\\end{tikzpicture}']


class CV(Page):
    """
    Define specific CV properties.
    """
    def __init__(self, layout):
        name = 'Curriculum vitae'
        super().__init__(name, layout)
        self.pages = layout['pages']
        self.box_top = layout['box_top']
        self.box_bottom = layout['box_bottom']
        self.box_left = layout['box_left']
        self.box_right = layout['box_right']
        self.include_photo = layout['include_photo']
        self.title_on_every_page = layout['title_on_every_page']


class Letter(Page):
    """
    Define specific letter properties.
    """
    def __init__(self, letter):
        name = 'Letter'
        super().__init__(name, letter)
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
    """
    Define address properties.
    """
    def __init__(self, dict_address):
        self.street = dict_address['street']
        self.house = dict_address['house']
        self.postal_code = dict_address['postal_code']
        self.city = dict_address['city']
        self.country = dict_address['country']

    def oneline(self):
        """
        Write address as single-line LaTeX output.
        """
        return '{} {}, {} {}'.format(self.street, self.house, self.postal_code, self.city)

    def twoline(self):
        """
        Write address as two-line LaTeX output.
        """
        return '{} {}\\\\{} {}'.format(self.street, self.house, self.postal_code, self.city)


class Backaddress(object):
    """
    Define backaddress properties.
    """
    def __init__(self, dict_pers, dict_address):
        self.first_name = dict_pers['first_name']
        self.family_name = dict_pers['family_name']
        self.street = dict_address['street']
        self.house = dict_address['house']
        self.postal_code = dict_address['postal_code']
        self.city = dict_address['city']
        self.country = dict_address['country']

    def oneline(self, space='1.5cm', separator='$\\bullet$'):
        """
        Write backaddress as single-line LaTeX output.
        """
        return '{0} {1}\\hspace{{{6}}}{7}\\hspace{{{6}}}{2} {3}\\hspace{{{6}}}{7}\\hspace{{{6}}}{4} {5}'.format(self.first_name, self.family_name, self.street, self.house, self.postal_code, self.city, space, separator)


class Personal(object):
    """
    Define personal properties.
    """
    def __init__(self, dict_pers):
        self.birth_date = dict_pers['birth_date']
        self.birth_location_city = dict_pers['birth_location_city']
        self.citizenship = dict_pers['citizenship']
        self.marital_status = dict_pers['marital_status']
        self.children = dict_pers['children']

    def oneline(self, lang):
        """
        Write personal data as single-line LaTeX output.
        """
        if lang == 'en':
            about_str = 'Born {} in {}, {}, {}, {} children'.format(self.birth_date, self.birth_location_city, self.citizenship, self.marital_status, self.children)
        if lang == 'de':
            about_str = 'Geboren am {} in {}, {}, {}, {} Kinder'.format(self.birth_date, self.birth_location_city, self.citizenship, self.marital_status, self.children)
        return about_str

    def twoline(self, lang):
        """
        Write personal data as two-line LaTeX output.
        """
        if lang == 'en':
            about_str = 'Born {} in {},\\\\{}, {}, {} children'.format(self.birth_date, self.birth_location_city, self.citizenship, self.marital_status, self.children)
        if lang == 'de':
            about_str = 'Geboren am {} in {},\\\\{}, {}, {} Kinder'.format(self.birth_date, self.birth_location_city, self.citizenship, self.marital_status, self.children)
        return about_str


class Signature:
    """
    Define signature properties.
    """
    def __init__(self, name, x, y, height, text_above, text_below, filename):
        self.name = name
        self.x = x
        self.y = y
        self.height = height
        self.text_above = text_above
        self.text_below = text_below
        self.filename = filename

    def create(self):
        """
        Generate LaTeX output for signature.
        """
        if self.name == '':
            namestr = ''
        else:
            namestr = '({}) '.format(self.name)
        return '\\node {}[anchor=north west, text width=10cm] at ({}, {}) {{{}\\\\\\includegraphics[height={}cm]{{{}}}\\\\{}}};'.format(namestr, self.x, self.y, self.text_above, self.height, self.filename, self.text_below)


class Document:
    """
    Define document for enclosure
    """
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename

    def pagecount(self):
        """
        Count total page number of PDF document
        """
        with open(self.filename, 'rb') as pdf_file:
            pages = PdfFileReader(pdf_file).numPages
        return pages

    def include(self):
        """
        Generate LaTeX code for including document
        """
        l = []
        for page in range(self.pagecount()):
            l.append('\\begin{tikzpicture}')
            l.append('\t\\node [inner sep=0pt] at (current page.center) {{\\includegraphics[page={0}]{{{1}}}}};'.format(page+1, self.filename))
            l.append('\\end{tikzpicture}')
        return l


class Enclosure:
    """
    Define entire enclosure
    """
    def __init__(self, dict_files):
        self.files = dict_files

    def include(self):
        """
        Generate LaTeX code to include all documents
        """
        doc = []
        for key, value in self.files.items():
            doc = doc + Document(key, value).include()
        return doc
 

class PhotoArea(object):
    """
    Definition of photo area.
    """
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
    """
    General area definition.
    """
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


class Cell:
    """
    Definitions for a table cell
    """
    def __init__(self, name, xsep, ysep, align, minimum_width, minimum_height, text_width, text_height):
        self.name = name
        self.shape = 'rectangle'
        self.draw = 'none'
        self.inner_xsep = xsep
        self.inner_ysep = ysep
        self.align = align
        self.minimum_width = minimum_width
        self.minimum_height = minimum_height
        self.text_width = text_width
        self.text_height = text_height

    def set_style(self):
        """
        Assemble TikZ style
        """
        return '{}/.style={{{}, draw={}, inner xsep={}pt, inner ysep={}pt, align={}, minimum width={}cm, minimum height={}cm, text width={}cm, text height={}cm}},'.format(self.name, self.shape, self.draw, self.inner_xsep, self.inner_ysep, self.align, self.minimum_width, self.minimum_height, self.text_width, self.text_height) 


class Textbox:
    """
    General textbox definition
    """
    def __init__(self, settings, text):
        self.anchor = settings['anchor']
        self.x = settings['x']
        self.y = settings['y']
        self.inner_xsep = settings['inner_xsep']
        self.inner_ysep = settings['inner_ysep']
        self.font_size = settings['font_size']
        self.case = settings['case']
        self.text_width = settings['text_width'] 
        self.align = settings['align'] 
        self.yshift = settings['yshift']
        self.color = settings['color']
        if self.case == 'upper':
            self.text = text.upper()
        elif self.case == 'lower':
            self.text = text.lower()
        else:
            self.text = text

    def create(self):
        return '\\node [anchor={0}, inner xsep={1}pt, inner ysep={2}, font=\\{3}, yshift={4}cm, text width={5}cm, align={6}, color={7}] at ({8}, {9}) {{{10}}};'.format(self.anchor, self.inner_xsep, self.inner_ysep, self.font_size, self.yshift, self.text_width, self.align, self.color, self.x, self.y, self.text)


class Table:
    """
    Definitions for a table (matrix of nodes)
    """
    def __init__(self, settings, items):
        self.name = settings['name']
        self.anchor = settings['anchor']
        self.x = settings['x']
        self.y = settings['y']
        self.font_size = settings['font_size']
        self.column_styles = settings['column_styles']
        self.items = items

    def head(self):
        """
        Assemble table header using table properties and column styles
        """
        l = [
                '% {}'.format(self.name.upper()),
                '\\matrix ({}) at ({}, {}) ['.format(self.name, self.x, self.y),
                '\t' + 'anchor={},'.format(self.anchor),
                '\t' + 'font=\\{},'.format(self.font_size),
                '\t' + 'matrix of nodes,',
                ]
        for i, style in enumerate(self.column_styles):
            l.append('\t' + 'column {}/.style={{nodes={{{}}}}},'.format(i+1, style))
        l.append('\t]{')
        return l

    def add_row(self, entries):
        """
        Add single row to a table
        """
        row = '\t'
        for entry in entries:
            row = row + '\\node {{{}}}; & '.format(entry)
        row = row[:-3]
        row = row + '\\\\'
        return row

    def foot(self):
        """
        Footer line
        """
        return '\t};'

    def assemble(self):
        """
        Assemble complete table
        """
        table = self.head()
        for item in self.items:
            table.append(self.add_row(item))
        table.append(self.foot())
        return table


class Itemize:
    """
    Define itemize environment
    """
    def __init__(self, label, labelsep, leftmargin, topsep, itemindent, itemsep, items):
        self.label = label
        self.labelsep = labelsep
        self.leftmargin = leftmargin
        self.topsep = topsep
        self.itemindent = itemindent
        self.itemsep = itemsep
        self.items = items

    def generate(self):
        """
        Generate LaTeX code for itemize environment
        """
        l = [
                '\\begin{itemize}[',
                '\t' + 'topsep={},'.format(self.topsep),
                '\t' + 'leftmargin={},'.format(self.leftmargin),
                '\t' + 'labelsep={},'.format(self.labelsep),
                '\t' + 'itemindent={},'.format(self.itemindent),
                '\t' + 'itemsep={},'.format(self.itemsep),
                '\t' + 'label={},'.format(self.label),
                '\t' + ']',
                ]
        for item in self.items:
            l.append('\t\item {}'.format(item))
        l.append('\\end{itemize}')
        l = ''.join(l)
        return l


class Box(object):
    """
    General box definition.
    """
    def __init__(self, color, width, height):
        self.color = color
        self.width = width
        self.height = height


class SkillCircle(object):
    """
    Definition of a skill circle.
    """
    def __init__(self, dict_skill_circle):
        self.radius = dict_skill_circle['radius']
        self.fillcolor = dict_skill_circle['fillcolor']
        self.opencolor = dict_skill_circle['opencolor']
        self.linecolor = dict_skill_circle['linecolor']
        self.showline = dict_skill_circle['showline']


class SkillLayout(object):
    """
    Definition of skill layout.
    """
    def __init__(self, dict_skill_layout):
        self.number = dict_skill_layout['circle_number']
        self.distance = dict_skill_layout['circle_distance']
        self.show_circles = dict_skill_layout['show_circles']


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
    with open(config_dir, 'w') as f:
        json.dump(settings_dict, f, indent=4)

