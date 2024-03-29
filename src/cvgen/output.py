#!/usr/bin/env python3
"""Functions for generating the output file."""

import cvdata as cv
import geometry as geo
import functions as fn
import numpy as np
import pandas as pd
from datetime import datetime
from PyPDF2 import PdfFileMerger


def mergepdfs(pdflist, target):
    """Merge all PDFs."""
    merger = PdfFileMerger()
    for pdf in pdflist:
        merger.append(pdf)
    merger.write(target)
    merger.close()


def tikzset(config_cell_styles):
    """Define styles."""
    l = ['\\tikzset{']
    for key, value in config_cell_styles.items():
        l.append('\t' + geo.Cell(**value).set_style())
    skillcirc_set = {
            'total': 5,
            'distance': 0.4,
            'radius': 0.3,
            'fillcolor': 'Blues-K',
            'opencolor': 'Greys-G',
            'linecolor': '',
            }
    l = l + geo.SkillCircles(**skillcirc_set).define()
#    l2 = [
#        '\t' + r'circfull/.style={draw=none, fill=Blues-K},',
#        '\t' + r'circopen/.style={draw=none, fill=Greys-G},',
#        '\t' + r'pics/skillmax/.style n args={3}{code={',
#        '\t\t' + r'\foreach \x in {1, ..., #1} {\filldraw[circfull] (#2*\x, 0) circle [radius=#3 mm];};',
#        '\t\t' + r'}',
#        '\t' + r'},',
#        '\t' + r'pics/skillmin/.style n args={3}{code={',
#        '\t\t' + r'\foreach \x in {1, ..., #1} {\filldraw[circopen] (#2*\x, 0) circle [radius=#3 mm];};',
#        '\t\t' + r'}',
#        '\t' + r'},',
#        '\t' + r'pics/skill/.style n args={5}{code={',
#        '\t\t' + r'\foreach \x in {1, ..., #1} {\filldraw[circfull] (#4*\x, 0) circle [radius=#5 mm];};',
#        '\t\t' + r'\foreach \x in {#2, ..., #3} {\filldraw[circopen] (#4*\x, 0) circle [radius=#5 mm];};',
#        '\t\t' + r'}',
#        '\t' + r'},',
    l.append('}')
    return l


def assemble_letter(dict_letter, letter_text, dict_pers, dict_cont, company,
                    icons, encl, dict_set, draft, language):
    """Assemble LaTeX code for letter."""
#    for key, value in dict_letter.items():
#        dict_letter[key] = fn.cm_add(value)
    letter = geo.Letter(dict_letter)
    # Language-dependent settings
    if language == 'en':
        subject_str = 'Application as'
        closing_str = 'Yours sincerely'
        enclosure_str = 'Enclosed:'
    elif language == 'de':
        subject_str = 'Bewerbung als'
        closing_str = 'Mit freundlichen Grüßen,'
        enclosure_str = 'Anlagen:'
    else:
        subject_str = 'Application as'
        closing_str = 'Yours sincerely'
        enclosure_str = 'Enclosed'
        print('[error] Language not supported')
    # Layout
    l = [
        r'% === LETTER ===',
        r'\begin{tikzpicture}[',
        '\t' + r'inner xsep=0pt,',
        '\t' + r'inner ysep=0pt,',
        '\t' + r'trim left=0pt,',
        '\t' + r'trim right={\paperw cm},',
        '\t' + r']',
        '\t' + r'\begin{pgfonlayer}{background}',
        '\t\t\\fill [fill=none] (0, 0) rectangle ({}, {});'.format(letter.width, letter.height),
        '\t' + r'\end{pgfonlayer}',
        ]
    # Area highlighting
    if draft is True:
        l2 = [
             '\t' + r'% AREA HIGHLIGHTING',
             '\t' + r'\begin{pgfonlayer}{forebackground}',
             '\t\t' + r'\begin{scope}[',
             '\t\t\t' + 'fill={}, draw={},'.format(letter.draft_highlight_color, 'black'),
             '\t\t\t' + ']',
             '\t\t\t' + r'% |- Border',
             '\t\t\t\\filldraw ({}, {}) rectangle ({}, {});'.format(letter.border_left, letter.border_bottom, letter.width-letter.border_right, letter.height-letter.border_top),
             '\t\t\t' + r'% |- Address field, total window',
             '\t\t\t' + '\\filldraw ({}, {}) rectangle +({}, {});'.format(letter.address_x, letter.address_y, letter.address_width, letter.address_height),
             '\t\t\t' + r'% |- Address field, recipient area',
             '\t\t\t' + '\\filldraw ({}, {}) rectangle +({}, {});'.format(letter.border_left, letter.address_y, letter.address_width-0.5, 2.73),
             '\t\t\t' + r'% |- Date field',
             '\t\t\t' + '\\filldraw ({}, {}) rectangle ({}, {});'.format(letter.border_left, letter.folding_mark_1_y, letter.width-letter.border_right, letter.address_y),
             '\t\t\t' + r'% |- Subject field',
             '\t\t\t' + '\\filldraw ({}, {}) rectangle ({}, {});'.format(letter.border_left, letter.subject_y, letter.width-letter.border_right, letter.folding_mark_1_y),
             '\t\t\t' + r'% |- Text area',
             '\t\t\t\\filldraw ({}, {}) rectangle ({}, {});'.format(letter.border_left, letter.border_bottom, letter.width-letter.border_right, letter.text_y),
             '\t\t' + r'\end{scope}',
             '\t' + r'\end{pgfonlayer}',
             ]
        l = l + l2
    # Marks
    l2 = [
         '\t' + r'% MARKS',
         '\t' + r'\begin{pgfonlayer}{foreground}',
         '\t\t' + r'% |- Backaddress separator',
         '\t\t' + '\\draw [line width={}] ({}, {}) -- +({}, 0);'.format(letter.backaddress_sepline_thickness, letter.address_x, letter.backaddress_y, letter.address_width),
         '\t\t' + r'% |- Perforation mark',
         '\t\t' + '\\draw [line width={}] ({}, {}) -- +({}, 0);'.format(letter.perforation_mark_thickness, letter.perforation_mark_x, letter.perforation_mark_y, letter.perforation_mark_width),
         '\t\t' + r'% |- Folding mark 1',
         '\t\t' + '\\draw [line width={}] ({}, {}) -- +({}, 0);'.format(letter.folding_mark_1_thickness, letter.folding_mark_1_x, letter.folding_mark_1_y, letter.folding_mark_1_width),
         '\t\t' + r'% |- Folding mark 2',
         '\t\t' + '\\draw [line width={}] ({}, {}) -- +({}, 0);'.format(letter.folding_mark_2_thickness, letter.folding_mark_2_x, letter.folding_mark_2_y, letter.folding_mark_2_width),
         '\t' + r'\end{pgfonlayer}',
         ]
    l = l + l2
    # Content
    include_backaddress = True
    if include_backaddress is True:
        backaddress = geo.Backaddress(dict_pers, dict_cont)
        l3 = [
            '\t' + r'% CONTENT',
            '\t' + r'% |- Backaddress',
            '\t' + '\\node [anchor=south west, text width=9cm, align=center, font=\\scriptsize] at ({}, {}) {{{}}};'.format(letter.address_x, letter.backaddress_y, backaddress.oneline('8pt', '$\\bullet$'))
            ]
        l = l + l3
    recipient = company.address()
    # Recipient address
    l.append('\t' + r'% |- Recipient address')
    l.append('\t\\node [anchor=north west, minimum width={0}cm, minimum height=2.73cm, text width={0}cm, align=left] at ({1}, {2}) {{{3}}};'.format(letter.address_width, letter.border_left, letter.backaddress_y, recipient))
    # Headline
    x = letter.width-letter.border_right
    y = letter.height-letter.border_top
    fullwidth = True
    anchor = 'south east'
    size = 'Large'
    headline = '{}~{}~{}'.format(dict_pers['title'], dict_pers['first_name'], dict_pers['family_name'])
    l.append('\t' + r'% |- Headline')
    l.append('\t' + letter.add_title(headline, size, 'right', 'black', 0.1))
    l.append('\t' + r'% |- Headline separator')
    l.append('\t' + letter.add_headsepline(0.1, 'Blues-K', fullwidth))
#    l.append('\t' + r'% |- Footline separator')
#    l.append('\t' + letter.add_footsepline(0.1, 'Blues-K', fullwidth))
    # Sender address
    l.append('\t' + r'% |- Sender address')
    x = letter.width-letter.border_right
    y = letter.height-letter.border_top
    anchor = 'north east'
    bsize = 'normalsize'
    l4 = [
            '\t\\begin{{scope}}[row sep=-\\pgflinewidth, column sep=-\\pgflinewidth, text height=0.0cm, minimum height=0.5cm, font=\\{}]'.format(bsize),
            '\t\t\\matrix at ({}, {}) ['.format(x, y-0.15),
            '\t\t\t' + 'anchor={},'.format(anchor),
            '\t\t\t' + r'matrix of nodes,',
            '\t\t\t' + r'column 1/.style={nodes={cell8}},',
            '\t\t\t' + r'column 2/.style={nodes={cell9}},',
            '\t\t\t' + r']{',
            ]
    contact = cv.Contact(dict_cont)
    address_data = geo.Address(dict_cont)
    address = address_data.twoline()
    vspace2 = 0.5
    l4.append('\t\t\t\\node [text depth={0}cm] {{{1}}}; & \\node [text depth={0}cm] {{{2}}};\\\\'.format(vspace2, address, icons['address']))
    l4.append('\t\t\t\\node {{{}}}; & \\node {{{}}};\\\\'.format(contact.phone, icons['phone']))
    clickable = True
    if clickable is True:
        email_subject = 'Ihre Bewerbung bei {}'.format(company.name)
        email = fn.make_link_email(contact.email, '', email_subject)
        l4.append('\t\t\t\\node {{{0}}}; & \\node {{{1}}};\\\\'.format(email, icons['mail']))
#        l4.append('\t\t\t\\node {{\\href{{mailto:{0}?subject={1}}}{{{0}}}}}; & \\node {{{2}}};\\\\'.format(contact.email, email_subject, icons['mail']))
    else:
        l4.append('\t\t\t\\node {{{}}}; & \\node {{{}}};\\\\'.format(contact.email, icons['mail']))
    l4.append('\t\t\t' + r'};')
    l4.append('\t' + r'\end{scope}')
    # Date field
    today = datetime.today().strftime(dict_set['date_format'])
    date = '{}, {}'.format(contact.city, today)
    l4.append('\t' + r'% |- Date field')
    l4.append('\t' + '\\node [anchor=south east] at ({}, {}) {{{}}};'.format(letter.width-letter.border_right, letter.folding_mark_1_y, date))
    # Subject field
    if company.tag_number == '':
        subject = '{} {}'.format(subject_str, company.position)
    else:
        subject = '{} {} ({})'.format(subject_str, company.position, company.tag_number)
    l4.append('\t' + r'% |- Subject field')
    l4.append('\t' + '\\node [anchor=south west] at ({}, {}) {{\\bf {}}};'.format(letter.border_left, letter.subject_y, subject))
    l = l + l4
    # Letter text
    l.append('\t' + r'% |- Letter text')
    l.append('\t\\node (textbox) [anchor=north west, text width={}cm, align=justify] at ({}, {}) {{'.format(letter.text_width, letter.border_left, letter.text_y))
    for line in letter_text:
        l.append('\t\t' + line)
    l.append('\t' + r'};')
    # Closing and signature
    l.append('\t' + r'% |- Closing and signature')
#    closing = 'Mit freundlichen Grüßen,'
    below = '{} {}'.format(dict_pers['first_name'], dict_pers['family_name'])
    name = 'closing'
    signature = geo.Signature(name, letter.border_left, letter.border_bottom+letter.closing_y_shift, 1.3, closing_str, below, dict_pers['signature'])
    l.append(signature.create())
#    l.append('\t' + '\\node (closing) [anchor=north west, text width=10cm, yshift={}cm] at (textbox.south west) {{{}\\\\\\includegraphics[height=1.3cm]{{{}}}\\\\{} {}}};'.format(letter.closing_y_shift, closing, signature, dict_pers['first_name'], dict_pers['family_name']))
    # Enclosure
    l.append('\t' + r'% |- Enclosure')
#    enclosure = 'Anlagen:'
    for item in encl:
        enclosure_str = '{} {},'.format(enclosure_str, item)
    enclosure_str = enclosure_str[:-1]
    l.append('\t\\node [anchor=north west, text width={}cm, yshift={}cm] at (closing.south west) {{{}}};'.format(letter.text_width, letter.enclosure_y_shift, enclosure_str))
    l.append(r'\end{tikzpicture}')
    return l


def assemble_latex(outfile, version_str, config_file_geo, config_file_data, config_file_encl, text, microtype, include_meta, encl, draft, enclosure_latex, config_file_preamble, config_file_cell_styles, config_file_company, language, config_file_layers, config_file_skills):
    """Read out config values, create objects, and assemble LaTeX code."""

    def declare_variables():
        """Define variables for geometry data."""
        l = [
            r'\paperw = {}; % paper width'.format(cvl.width),
            r'\paperh = {}; % paper height'.format(cvl.height),
            ]
        if cvl.box_left is True:
            l.append(r'\boxlw = {}; % box left width'.format(box_left.width))
        if cvl.box_right is True:
            l.append(r'\boxrw = {}; % box right width'.format(box_right.width))
        if cvl.box_top is True:
            l.append(r'\boxth = {}; % box top height'.format(box_top.height))
        if cvl.box_bottom is True:
            l.append(r'\boxbh = {}; % box bottom height'.format(box_bottom.height))
        return l

    def draw_background():
        """Draw background and boxes."""
        l = [
            '\t\t' + r'\begin{pgfonlayer}{background}',
            '\t\t\t' + '\\fill[fill={}] (0, 0) rectangle (\\paperw, \\paperh);'.format(cvl.background_color),
            '\t\t' + r'\end{pgfonlayer}',
            '\t\t' + r'\begin{pgfonlayer}{forebackground}',
            ]
        if cvl.box_left is True:
            l.append('\t\t\t' + '\\fill[fill={}] (0, 0) rectangle (\\boxlw, \\paperh); % box left'.format(box_left.color))
        if cvl.box_right is True:
            l.append('\t\t\t' + '\\fill[fill={}] ({}, 0) rectangle (\\paperw, \\paperh); % box right'.format(box_right.color, cvl.width-box_right.width))
        if cvl.box_top is True:
            l.append('\t\t\t' + '\\fill[fill={}] (0, {}) rectangle (\\paperw, \\paperh); % box top'.format(box_top.color, cvl.height-box_top.height))
        if cvl.box_bottom is True:
            l.append('\t\t\t' + '\\fill[fill={}] (0, 0) rectangle (\\paperw, \\boxbh); % box bottom'.format(box_bottom.color))
        l.append('\t\t' + r'\end{pgfonlayer}')
        return l

    # Read config files
    config_data = fn.read_config(config_file_data)
    config_company = fn.read_config(config_file_company)
    config_geo = fn.read_config(config_file_geo)
    config_preamble = fn.read_config(config_file_preamble)
    config_cell_styles = fn.read_config(config_file_cell_styles)
    config_layers = fn.read_config(config_file_layers)
    dict_layout = config_geo['cv']['layout']
    dict_letter = config_geo['letter']
    dict_box = config_geo['cv']['boxes']
    dict_box_top = dict_box['box_top']
    dict_box_bottom = dict_box['box_bottom']
    dict_box_left = dict_box['box_left']
    dict_box_right = dict_box['box_right']
    dict_areas = config_geo['cv']['areas']
    structure = config_geo['structure']
    cvl = geo.CV(dict_layout)
    cv_pages = cvl.pages
    box_top = geo.Box(color=dict_box_top['color'], width=cvl.width,
                      height=dict_box_top['size'])
    box_bottom = geo.Box(color=dict_box_bottom['color'], width=cvl.width,
                         height=dict_box_bottom['size'])
    box_left = geo.Box(color=dict_box_left['color'],
                       width=dict_box_left['size'], height=cvl.height)
    box_right = geo.Box(color=dict_box_right['color'],
                        width=dict_box_right['size'], height=cvl.height)
    company = cv.Company(config_company)
    if language == 'en':
        languages_str = 'Languages'
        licenses_str = 'Licenses'
    elif language == 'de':
        languages_str = 'Sprachen'
        licenses_str = 'Führerscheine'

    # General settings
    dict_set = config_geo['general']

    # Icons
    icons = config_geo['icons']
    icon_names = config_data['Contact']['icons']

    # Assemble personal area
    dict_pers = config_data['Personal']
    person = cv.Personal(dict_pers)
    area_personal = geo.Area(dict_areas['personal'])
    personal_title_set = {
        'name': 'personal_title',
        'anchor': area_personal.anchor,
        'x': box_left.width,
        'y': area_personal.pos_y,
        'at': '',
        'inner_xsep': 8,
        'inner_ysep': 0,
        'text_width': 8,
        'align': 'left',
        'font_size': area_personal.head_font_size,
        'case': area_personal.head_case,
        'yshift': area_personal.head_vspace,
        'color': area_personal.color,
        }
    personal_body_set = {
        'name': 'personal_body',
        'anchor': area_personal.anchor,
        'x': box_left.width,
        'y': area_personal.pos_y,
        'at': '',
        'inner_xsep': 8,
        'inner_ysep': 0,
        'text_width': 8,
        'align': 'left',
        'font_size': area_personal.body_font_size,
        'case': 'mixed',
        'yshift': -0.6,
        'color': area_personal.color,
        }
    pers = [
        '% PERSONAL AREA',
        '% |- Title:',
        ]
    pers.append(geo.Textbox(personal_title_set, area_personal.title).create())
    pers.append('% |- Items:')
    if area_personal.style == 'oneline':
        about_str = geo.Personal(dict_pers).oneline(language)
    elif area_personal.style == 'twoline':
        about_str = geo.Personal(dict_pers).twoline(language)
    pers.append(geo.Textbox(personal_body_set, about_str).create())

    # Assemble title
    x = cvl.width-cvl.border_right
    y = cvl.height-cvl.border_top
    area_title = geo.Area(dict_areas['title'])
    titlebox_title_set = {
        'name': 'titlebox_title',
        'anchor': area_title.anchor,
        'x': area_title.pos_x,
        'y': y,
        'at': '',
        'inner_xsep': 8,
        'inner_ysep': 4,
        'font_size': area_title.head_font_size,
        'text_width': 5.3,
        'align': 'right',
        'case': area_title.head_case,
        'yshift': area_title.head_vspace,
        'color': area_title.color,
        }
    titlebox = geo.Textbox(titlebox_title_set, area_title.title).create()
    title = []
    title.append(titlebox)

    # Headline
    fullwidth = True
    size = 'Large'
    headline = '{}~{}~{}'.format(person.title, person.first_name,
                                 person.family_name)
#    title = []
    title.append('\t' + r'% |- Headline')
    title.append('\t' + cvl.add_title(headline, size, 'right', 'black', 0.1))
    if area_title.head_sepline is True:
        title.append('\t' + r'% |- Headline separator')
        title.append('\t' + cvl.add_headsepline(0.1, 'Blues-K', fullwidth))
#    l.append('\t' + r'% |- Footline separator')
#    l.append('\t' + cvl.add_footsepline(0.1, 'Blues-K', fullwidth))
#    title.append('% TITLE')
#    title.append(cvl.add_headsepline(0.1, 'Blues-K'))
#    title.append(cvl.add_title(0.1, 'Blues-K'))
#            '\\node [anchor={}, font=\\{}] at ({}, {}) {{{} {}}};'.format(anchor, hsize, x, y, person.first_name, person.family_name),
#            ]
#        title.append('\\draw [draw={}, line width=1pt] ({}, {}) -- ({}, {});'.format(area_title.color, x, y-0.8, l, y-0.8))
#    title.append('\\node [anchor={}, font=\\{}, text height=0.6cm] at ({}, {}) {{{}}};'.format(anchor, bsize, x, y-0.8, area_title.title))

    # Assemble photo
    dict_photo = config_geo['cv']['areas']['photo']
    photo_file = config_data['Personal']['photo']
    area_photo = geo.PhotoArea(dict_photo)
    x = cvl.width-cvl.border_right
    y = cvl.height-cvl.border_top-0.2
    thickness = 0.1
    anchor = 'north east'
    width = area_photo.width
    if area_photo.border is True:
        border_color = area_photo.border_color
    else:
        border_color = 'none'
    photo = [
            '% PHOTO AREA',
            r'\begin{scope}',
#            '\t' + '\\clip  ({}, {}) rectangle ({}, {});'.format(x, y, x+width, y-height),
            '\t\\node[anchor={}, inner sep=0, draw={}, line width={}cm] (image) at ({}, {}) {{\\includegraphics[width={}cm]{{{}}}}};'.format(anchor, border_color, thickness, x, y, width, photo_file),
#            '\t' + '\\draw [draw={}, line width={}] ({}, {}) rectangle ({}, {});'.format(border_color, area_photo.border_width, x, y, x+width, y-height),
            r'\end{scope}',
            ]

    # Contact
    area_contact = geo.Area(dict_areas['contact'])
    dict_contact = config_data['Contact']
    contact = cv.Contact(dict_contact)
    address_data = geo.Address(dict_contact)
    address = address_data.twoline()
    contact_title_set = {
        'name': 'contact_title',
        'anchor': area_contact.anchor,
        'x': box_left.width,
        'y': area_contact.pos_y,
        'at': '',
        'inner_xsep': 8,
        'inner_ysep': 0,
        'font_size': area_contact.head_font_size,
        'text_width': 8,
        'align': 'left',
        'case': area_contact.head_case,
        'yshift': area_contact.head_vspace,
        'color': area_contact.color,
        }
    contact_set = {
        'name': 'Contact',
        'anchor': area_contact.anchor,
        'x': area_contact.pos_x,
        'y': area_contact.pos_y,
        'at': '',
        'font_size': area_contact.body_font_size,
        'column_styles': ['cell3', 'cell4'],
        }
    language_corr = 'de'
    if language_corr == 'en':
        email_subject = 'Your application at {}'.format(company.name)
    elif language_corr == 'de':
        email_subject = 'Ihre Bewerbung bei {}'.format(company.name)
    else:
        print('[error] Language not supported.')
    email = fn.make_link_email(contact.email, '', email_subject)
    items = [
            [icons['address'], address],
            [icons['phone'], contact.phone],
            [icons['mail'], email],
            ]
    for key, value in contact.weblinks.items():
        if key not in area_contact.hide_items:
            key = key.replace('_', r'\_')
            value = value.replace('_', r'\_')
            if (area_contact.hyperlinks is True) and (value != ''):
                value = fn.make_link_url(value, True, True, '')
            items.append([icons[icon_names[key]], value])
    cont = geo.Table(contact_set, items).assemble()
    cont.insert(0, geo.Textbox(contact_title_set, area_contact.title).create())

    # Career
    dict_career = config_data['Career']
    car_items = []
    for car_item in dict_career.values():
        car_items.append(cv.CareerItem(car_item))
    area_career = geo.Area(dict_areas['career'])
    career_title_set = {
        'name': 'career_title',
        'anchor': area_career.anchor,
        'x': box_left.width,
        'y': area_career.pos_y,
        'at': '',
        'inner_xsep': 8,
        'inner_ysep': 0,
        'font_size': area_career.head_font_size,
        'text_width': 8,
        'align': 'left',
        'case': area_career.head_case,
        'yshift': area_career.head_vspace,
        'color': area_career.color,
        }
    career_set = {
        'name': 'Career',
        'anchor': area_career.anchor,
        'x': area_career.pos_x,
        'y': area_career.pos_y,
        'at': '',
        'font_size': area_career.body_font_size,
        'column_styles': ['cell1', 'cell2', 'cell7'],
        }
    item_set = {
        'label': '\\textcolor{Blues-K}{\\Large\\textopenbullet}',
        'labelsep': '0.5em',
        'leftmargin': '1.2em',
        'topsep': '0.7em',
        'itemindent': '0.0em',
        'itemsep': '-0.2em',
        }
    items = []
    for car_item in reversed(car_items):
        desc = fn.makelist(car_item.description)
        if isinstance(desc, list):
            description = geo.Itemize(**item_set, items=desc).generate()
        else:
            description = desc
        items.append(['{}\\,--\\,{}'.format(car_item.start_date, car_item.end_date), '{}\\\\{}'.format(car_item.company_name, description), car_item.role])
    car = geo.Table(career_set, items).assemble()
    car.insert(0, geo.Textbox(career_title_set, area_career.title).create())

    # Education
    dict_edu = config_data['Education']
    edu_items = []
    for edu_item in dict_edu.values():
        if 'start_date' in edu_item:
            edu_items.append(cv.EduPeriodItem(edu_item))
        else:
            edu_items.append(cv.EduEventItem(edu_item))
    area_edu = geo.Area(dict_areas['education'])
    edu_title_set = {
        'name': 'edu_title',
        'anchor': 'north west',
        'x': box_left.width,
        'y': area_edu.pos_y,
        'at': '',
        'inner_xsep': 8,
        'inner_ysep': 0,
        'text_width': 8,
        'align': 'left',
        'font_size': area_edu.head_font_size,
        'case': area_edu.head_case,
        'yshift': area_edu.head_vspace,
        'color': area_edu.color,
        }
    edu_set = {
        'name': 'Education',
        'anchor': area_edu.anchor,
        'x': area_edu.pos_x,
        'y': area_edu.pos_y,
        'at': '',
        'font_size': area_edu.body_font_size,
        'column_styles': ['cell1', 'cell2', 'cell7'],
        }
    item_set = {
        'label': '\\textcolor{Blues-K}{\\Large\\textopenbullet}',
        'labelsep': '0.5em',
        'leftmargin': '1.2em',
        'topsep': '0.1em',
        'itemindent': '0.0em',
        'itemsep': '-0.2em',
        }
    items = []
    for edu_item in reversed(edu_items):
        desc = fn.makelist(edu_item.description)
        if isinstance(desc, list):
            description = geo.Itemize(**item_set, items=desc).generate()
        else:
            description = desc
        if isinstance(edu_item, cv.EduPeriodItem):
            items.append(['{}\\,--\\,{}'.format(edu_item.start_date, edu_item.end_date), '{}\\\\{}'.format(edu_item.school_name, description), edu_item.role])
        else:
            items.append([edu_item.date, '{}\\\\{}'.format(edu_item.school_name, description), edu_item.graduation])
    items_page_1 = items[:2]   # restrict to first 2 elements (first page)
    items_page_2 = items[2:]
    edu = geo.Table(edu_set, items_page_1).assemble()
    edu.insert(0, geo.Textbox(edu_title_set, area_edu.title).create())
    edu2_set = {
            'name': 'Education',
            'anchor': area_edu.anchor,
            'x': area_edu.pos_x,
            'y': 27,
            'at': '',
            'font_size': area_edu.body_font_size,
            'column_styles': ['cell1', 'cell2', 'cell7'],
            }
    edu2 = geo.Table(edu2_set, items_page_2).assemble()

    # Skills
    dict_skills2 = fn.read_config(config_file_skills)
    df_skills = pd.DataFrame.from_dict(dict_skills2, orient='index')
    # Vectorize function fn.make_level_numeric
    num = np.vectorize(fn.make_level_numeric)
    df_skills['level_numeric'] = num(df_skills['level'], df_skills['maxlevel'])
    # Vectorize function fn.make_skill_circles
    circ = np.vectorize(fn.make_skill_circles)
    # Add column 'circles' with LaTeX code for circles
    df_skills['circles'] = circ(df_skills['level'], df_skills['maxlevel'])
    # Convert values of 'level' and 'maxlevel' to strings
    df_skills['level'] = df_skills['level'].astype(str)
    df_skills['maxlevel'] = df_skills['maxlevel'].astype(str)

    # Get unique groups
    skill_groups = df_skills['group'].drop_duplicates()
    skill_groups = skill_groups[:-1]
    # Create list of group dataframes and keep order
    grouped = df_skills.groupby(['group'], as_index=True, sort=False)
    # groups = [grouped.get_group(x) for x in grouped.groups]
    # print(groups)
#    for i, group in enumerate(skill_groups):
#        groups.append(df_skills.groupby(['group'], as_index=False))
#        print(groups[i].groups)

    # section_header_style = 'left'
    # item_style = 'onerow'
    item_separator = ', '

    # print(groups[0])
    # for group in groups:

    #     if section_header_style == 'left':
    #         first_row = group.drop_duplicates(subset=['group'], keep='first')
    #         body = group.drop(index=group.index[0], axis=0)
    #         body['group'] = ''
    #         new = pd.concat([first_row, body])
    #         print(new)

#     # Group by groups and join corresponding names and levels to single line
#     separator = ', '
# #    level_style = 'numeric'
#     level_style = 'circles'
#     if level_style == 'numeric':
#         grouped = df_skills.groupby(['group'], as_index=True).agg({'name': separator.join, 'level_numeric': separator.join})
#     elif level_style == 'none':
#         grouped = df_skills.groupby(['group'], as_index=True).agg({'name': separator.join})
#     elif level_style == 'circles':
        
#         grouped = df_skills.groupby(['group'], as_index=True).agg({'name': '\\\\'.join, 'circles': '\\\\'.join})
#     else:
#         print('[error] Level style unknown. Choose between \"numeric\", \"circles\", and \"none\".')
    df_skills2 = df_skills[(df_skills['group'] != 'Zertifikate')]
    grouped = df_skills2.groupby(['group'], as_index=True).agg({'name': item_separator.join})
    # grouped = fn.make_table(df_skills, section_header_style, item_style, item_separator)

    # Restore initial group order
    grouped = grouped.reindex(skill_groups).reset_index()
    items = grouped.values.tolist()
    print(items)

    area_skills = geo.Area(dict_areas['skills'])
    skill_title_set = {
        'name': 'skill_title',
        'anchor': area_skills.anchor,
        'x': box_left.width,
        'y': area_skills.pos_y,
        'at': '',
        'inner_xsep': 8,
        'inner_ysep': 0,
        'text_width': 8,
        'align': 'left',
        'font_size': area_skills.head_font_size,
        'case': area_skills.head_case,
        'yshift': area_skills.head_vspace,
        'color': area_skills.color,
        }
    skill_set = {
        'name': 'Skills',
        'anchor': area_skills.anchor,
        'x': area_skills.pos_x,
        'y': area_skills.pos_y,
        'at': '',
        'font_size': area_skills.body_font_size,
        'column_styles': ['cell10', 'cell11'],
        # 'column_styles': ['cell10', 'cell11', 'cell11'],
        }
    item_set = {
        'label': '',
        'labelsep': '0.5em',
        'leftmargin': '0.0em',
        'topsep': '0.0em',
        'itemindent': '0.0em',
        'itemsep': '-0.2em',
        }

    # skills = []
    # skills.append(geo.Textbox(skill_title_set, area_skills.title).create())
    # last_group = ''
    # for i, group in enumerate(groups):
    #     group_name = group['group'][0]
    #     items = group[['name']].values.tolist()
    #     # items = group[['name', 'circles']].values.tolist()
    #     skill_set['name'] = group_name
    #     if last_group != '':
    #         skill_set['at'] = last_group + '.south west'
    #         skill_title_set['at'] = last_group + '.south west'
    #         skill_title_set['case'] = ''
    #     skills.append(geo.Textbox(skill_title_set, group_name).create())
    #     skills = skills + geo.Table(skill_set, items).assemble()
    #     last_group = group_name
    # print(skills)

    # skills = geo.Table(skill_set, items).assemble()

    df_skills3 = df_skills[(df_skills['group'] == 'Zertifikate')]
    df_skills3 = fn.make_section_header_left(df_skills3)
    print(df_skills3)
    grouped = df_skills3[['group', 'name']]
    items.append(['', ''])
    print(items)
    items = items + grouped.values.tolist()
    # skill_set['at'] = '{}.{}'.format(skill_set['name'], 'south')
    skills = geo.Table(skill_set, items).assemble()
    skills.insert(0, geo.Textbox(skill_title_set, area_skills.title).create())


#    row = []
#    group_items = []
#    for group in skill_groups:
#        group_items = df_skills[df_skills['group'] == group]
#        row.append(geo.List(group_items['name'].to_list(), separator=', ', orientation='row').generate())
#    print(row)
#    df_skills_groupsort = skill_groups.append(pd.DataFrame(row))
#    print(df_skills_groupsort)

#    for item in dict_skills2.values():
#        skill_objects.append(cv.SkillItem2(**item))
#    skill_groups = []
#    for item in skill_objects:
#        skill_groups.append(item.group)  # get all skill groups
#    skill_groups = list(set(skill_groups))  # get unique skill groups
#    items = []
#    for item in dict_skills2.values():
#        items.append([item['group'], item['name'], item['level']])

#    dict_skill_layout = config_geo['cv']['skills']['layout']
#    dict_skill_circle = config_geo['cv']['skills']['circle']
#    dict_skills = config_data['skills']
#    print(dict_skills)
#    skill_items = []
#    for skill_item in dict_skills.values():
#        skill_items.append(cv.SkillItem(skill_item['category'], skill_item['elements'], skill_item['level']))

#     for item in dict_skills.values():
#        skill_objects.append(cv.SkillItem(item))
#    skill_groups = []
#    for item in skill_objects:
#        skill_groups.append(item.group)  # get all skill groups
#    skill_groups = list(set(skill_groups))  # get unique skill groups

#    skill_layout = geo.SkillLayout(dict_skill_layout)


#    if skill_layout.show_circles is True:
#        for skill_item in skill_items:
#            desc = fn.makelist(skill_item.elements)
#            if isinstance(desc, list):
#                description = geo.Itemize(**item_set, items=desc).generate()
#            else:
#                elements = desc.split(',')
#                levels = skill_item.level.split(',')
#                for i, element in enumerate(elements):
#                    if i == 0:
#                        items.append([skill_item.category, element, levels[i]])
#                    else:
#                        items.append(['', element, levels[i]])
#            items.append([skill_item.category, description])
#        skills = geo.Table(skill_set, items).assemble()
#        skills.insert(0, geo.Textbox(skill_title_set, area_skills.title).create())
#    else:
#        for skill_item in skill_items:
#            desc = fn.makelist(skill_item.elements)
#            if isinstance(desc, list):
#                description = geo.Itemize(**item_set, items=desc).generate()
#            else:
#                description = desc
#            items.append([skill_item.category, description])
#        skills = geo.Table(skill_set, items).assemble()
#        skills.insert(0, geo.Textbox(skill_title_set, area_skills.title).create())
#    print(items)

    # skills = geo.Table(skill_set, items).assemble()
    # skills.insert(0, geo.Textbox(skill_title_set, area_skills.title).create())

    # Knowledge
    dict_know = config_data['knowledge']
    know_objects = []
    for item in dict_know.values():
        know_objects.append(cv.KnowledgeItem(item))
    know_groups = []
    for item in know_objects:
        know_groups.append(item.group)  # get all groups
    know_groups = list(set(know_groups))  # get unique groups
    area_know = geo.Area(dict_areas['knowledge'])
    know_title_set = {
        'name': 'know_title',
        'anchor': 'north west',
        'x': box_left.width,
        'y': area_know.pos_y,
        'at': '',
        'inner_xsep': 8,
        'inner_ysep': 0,
        'text_width': 8,
        'align': 'left',
        'font_size': area_know.head_font_size,
        'case': area_know.head_case,
        'yshift': area_know.head_vspace,
        'color': area_know.color,
        }
    know_set = {
        'name': 'Knowledge',
        'anchor': area_know.anchor,
        'x': area_know.pos_x,
        'y': area_know.pos_y,
        'at': '',
        'font_size': area_know.body_font_size,
        'column_styles': ['cell10', 'cell12', 'cell12'],
        }
    items = []
#    for group in know_groups:
#        row = ''
#        for obj in know_objects:
#            if obj.group == group:
#                row = row + obj.name + ', '
#        row = row[:-2]
#        items.append([group.replace('&', '\&'), row])
    first = True
    for obj in know_objects:
        if obj.group == languages_str:
            if first is True:
                items.append([obj.group, obj.name, obj.description])
                first = False
            else:
                items.append(['', obj.name, obj.description])
    items.append(['', '', ''])
    know = geo.Table(know_set, items).assemble()
    items = []
    know_set = {
        'name': 'Knowledge',
        'anchor': area_know.anchor,
        'x': area_know.pos_x,
        'y': area_know.pos_y-2.0,
        'at': '',
        'font_size': area_know.body_font_size,
        'column_styles': ['cell10', 'cell11', 'cell12'],
        }
    first = True
    for obj in know_objects:
        if obj.group == licenses_str:
            if first is True:
                items.append([obj.group, obj.name])
                first = False
            else:
                items.append(['', obj.name])
    know = know + geo.Table(know_set, items).assemble()
    know.insert(0, geo.Textbox(know_title_set, area_know.title).create())

    # # Certificates
    # dict_cert = config_data['certificates']
    # cert_objects = []
    # for item in dict_cert.values():
    #     cert_objects.append(cv.CertificateItem(item))
    # cert_groups = []
    # for item in cert_objects:
    #     cert_groups.append(item.group)  # get all groups
    # cert_groups = list(set(cert_groups))  # get unique groups
    # area_cert = geo.Area(dict_areas['certificates'])
    # cert_title_set = {
    #     'name': 'cert_title',
    #     'anchor': 'north west',
    #     'x': box_left.width,
    #     'y': area_cert.pos_y,
    #     'at': '',
    #     'inner_xsep': 8,
    #     'inner_ysep': 0,
    #     'text_width': 8,
    #     'align': 'left',
    #     'font_size': area_cert.head_font_size,
    #     'case': area_cert.head_case,
    #     'yshift': area_cert.head_vspace,
    #     'color': area_cert.color,
    #     }
    # cert_set = {
    #     'name': 'Certificates',
    #     'anchor': area_cert.anchor,
    #     'x': area_cert.pos_x,
    #     'y': area_cert.pos_y,
    #     'at': '',
    #     'font_size': area_cert.body_font_size,
    #     'column_styles': ['cell5', 'cell6'],
    #     }
    # items = []
    # for group in cert_groups:
    #     items.append([group.replace('&', '\&')])
    #     for obj in cert_objects:
    #         if obj.group == group:
    #             if area_cert.hyperlinks is True:
    #                 items.append(['\\href{{{}}}{{{}}}'.format(obj.name, obj.url)])
    #             else:
    #                 items.append([obj.name])
    # cert = geo.Table(cert_set, items).assemble()
    # cert.insert(0, geo.Textbox(cert_title_set, area_cert.title).create())

    # Metadata
    meta_set = {
            'first_name': person.first_name,
            'family_name': person.family_name,
            'title': person.title,
            'city': contact.city,
            'country': contact.country,
            'email': contact.email,
            'company': company.name,
            'position': company.position,
            'version': version_str,
            }

    # Insert variables into letter text
    variables = {
            '{company}': company.name,
            '{position}': company.position,
            '{tag_number}': company.tag_number,
            '{salary_expectation}': company.salary_expectation,
            '{earliest_join_date}': company.earliest_join_date,
            }
    for count, line in enumerate(text):
        text[count] = fn.replace_strings(variables, line)

    # Generate LaTeX preamble with or without metadata
    if include_meta is True:
        meta = cv.Metadata(**meta_set).generate()
    else:
        meta = None
    preamb = geo.Preamble(config_preamble['documentclass'],
                          config_preamble['packages'],
                          config_preamble['settings'], meta).generate(language)

    # Write to file
    with open(outfile, 'w', encoding='UTF-8') as f:
        # Write comment with program and version info
        f.write('% ===== LaTeX code generated by cvgen v{} =====\n'.format(version_str))
        # Write LaTeX preamble
        for line in preamb:
            f.write(line + '\n')
        f.write(r'\begin{document}' + '\n')
        # Write definitions of variables
        f.write('\t' + r'\tikzmath{' + '\n')
        for line in declare_variables():
            f.write('\t\t' + line + '\n')
        f.write('\t' + r'}' + '\n')
        # Write style definitions
        for line in tikzset(config_cell_styles):
            f.write('\t' + line + '\n')
        # Write layer declaration
        for line in fn.parse_layers(config_layers):
            f.write('\t' + line + '\n')
        if structure['letter'] is True:
            # Write letter
            for line in assemble_letter(dict_letter, text, dict_pers, dict_contact, company, icons, encl, dict_set, draft, language):
                f.write('\t' + line + '\n')
        if structure['cv'] is True:
            # Write CV
            for l in cvl.latex_head():
                f.write('\t' + l + '\n')
            for line in draw_background():
                f.write(line + '\n')
            f.write('\t\t' + r'\begin{pgfonlayer}{foreground}' + '\n')
            for c in cont:
                f.write('\t\t\t' + c + '\n')
            for i in photo:
                f.write('\t\t\t' + i + '\n')
            for t in title:
                f.write('\t\t\t' + t + '\n')
            for p in pers:
                f.write('\t\t\t' + p + '\n')
            for car_item in car:
                f.write('\t\t\t' + car_item + '\n')
            for edu_item in edu:
                f.write('\t\t\t' + edu_item + '\n')
            f.write('\t\t' + r'\end{pgfonlayer}' + '\n')
            for l in cvl.latex_foot():
                f.write('\t' + l + '\n')
            if cv_pages == 2:
                for l in cvl.latex_head():
                    f.write('\t' + l + '\n')
                for line in draw_background():
                    f.write(line + '\n')
                f.write('\t\t' + r'\begin{pgfonlayer}{foreground}' + '\n')
                f.write('\t\t' + '\\fill[fill=none] (0, 0) rectangle ({}, {});\n'.format(cvl.width, cvl.height))
                for t in title:
                    f.write('\t\t\t' + t + '\n')
                for edu_item in edu2:
                    f.write('\t\t\t' + edu_item + '\n')
                for skill in skills:
                    f.write('\t\t\t' + skill + '\n')
                for k in know:
                    f.write('\t\t\t' + k + '\n')
                closing = ''
                below = '{} {}'.format(dict_pers['first_name'], dict_pers['family_name'])
                name = 'closing2'
                signature = geo.Signature(name, cvl.border_left+3.1, cvl.border_bottom+1.4, 1.3, closing, below, dict_pers['signature'])
                f.write('\t\t\t' + signature.create() + '\n')
                f.write('\t\t' + r'\end{pgfonlayer}' + '\n')
                for l in cvl.latex_foot():
                    f.write('\t' + l + '\n')
            if enclosure_latex is True:
                enclosure = geo.Enclosure(config_file_encl).include()
                for l in enclosure:
                    f.write('\t' + l + '\n')
        f.write(r'\end{document}' + '\n')
