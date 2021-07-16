#!/usr/bin/env python3

import cvdata as cv
import geometry as geo
import functions as fn
from datetime import datetime
from PyPDF2 import PdfFileMerger


def mergepdfs(pdflist, target):
    merger = PdfFileMerger()
    for pdf in pdflist:
        merger.append(partfile)
    merger.write(target)
    merger.close()


def preamble(microtype, meta, include_meta):
    """
    Define LaTeX preamble with required packages included
    """
    l = [r'\documentclass[12pt, tikz, multi, crop]{standalone}']
    if include_meta is True:
        l.append(r'\usepackage{hyperxmp}')
    l.append(r'\usepackage[sfdefault, scaled=1.0098]{FiraSans}')
    l.append(r'\usepackage{newtxsf}')
    l.append(r'\usepackage{fontawesome5}')
    if microtype is True:
        l.append(r'\usepackage[activate={true, nocompatibility}, final, tracking=true, kerning=true, spacing=true, factor=1100, stretch=8, shrink=8]{microtype}')
    l2 = [
            r'\usepackage{tikz}',
            r'\usepackage{hyperref}',
            r'\usetikzlibrary{positioning, math, colorbrewer, backgrounds, matrix}',
            r'\standaloneenv{tikzpicture}',
            r'\hypersetup{',
            '\t' + r'colorlinks=true,',
            '\t' + r'urlcolor=Blues-K,',
            ]
    l = l + l2
    if include_meta is True:
        l3 = [
                '\t' + 'pdftitle={{Bewerbung bei {} als {}}},'.format(meta.company, meta.position),
                '\t' + r'pdfsubject={Bewerbung},',
                '\t' + 'pdfauthor={{{} {}}},'.format(meta.first_name, meta.family_name),
                '\t' + 'pdfauthortitle={{{}}},'.format(meta.title),
                '\t' + 'pdfcaptionwriter={{{} {}}},'.format(meta.first_name, meta.family_name),
                '\t' + 'pdfdate={{{}}},'.format(datetime.today().strftime('%Y-%m-%d')),
                '\t' + 'pdfproducer={{cvgen {}}},'.format(meta.version),
                '\t' + 'pdfcontactcity={{{}}},'.format(meta.city),
                '\t' + 'pdfcontactcountry={{{}}},'.format(meta.country),
                '\t' + 'pdfcontactemail={{{}}},'.format(meta.email),
                ]
        l = l + l3
    l.append(r'}')
    return l


def tikzset():
    """
    Define styles
    """
    l = [
        r'\tikzset{',
        '\t' + r'cell1/.style={rectangle, draw=black, inner xsep=0pt, inner ysep=4pt, text height=0.25cm, align=right, minimum width=2.0cm, text width=3.5cm},',
        '\t' + r'cell2/.style={rectangle, draw=black, inner xsep=6pt, inner ysep=4pt, text height=0.25cm, align=left, minimum width=1.5cm, text width=8.0cm},',
        '\t' + r'cell3/.style={rectangle, draw=black, inner xsep=0pt, inner ysep=4pt, text height=0.25cm, align=center, minimum width=0.6cm, text width=0.4cm},',
        '\t' + r'cell4/.style={rectangle, draw=black, inner xsep=3pt, inner ysep=4pt, text height=0.25cm, align=left, minimum width=1.0cm, text width=5.8cm},',
        '\t' + r'cell5/.style={rectangle, draw=black, inner xsep=0pt, inner ysep=4pt, text height=0.25cm, align=left, minimum width=0.6cm, text width=4.5cm},',
        '\t' + r'cell6/.style={rectangle, draw=black, inner xsep=0pt, inner ysep=4pt, text height=0.25cm, align=right, minimum width=1.0cm, text width=2.0cm},',
        '\t' + r'cell7/.style={rectangle, draw=black, inner xsep=0pt, inner ysep=4pt, text height=0.25cm, align=left, minimum width=1.0cm, text width=6.5cm},',
        '\t' + r'circfull/.style={draw=none, fill=Blues-K},',
        '\t' + r'circopen/.style={draw=none, fill=Greys-G},',
        '\t' + r'pics/skillmax/.style n args={3}{code={',
        '\t\t' + r'\foreach \x in {1, ..., #1} {\filldraw[circfull] (#2*\x, 0) circle [radius=#3 mm];};',
        '\t\t' + r'}',
        '\t' + r'},',
        '\t' + r'pics/skillmin/.style n args={3}{code={',
        '\t\t' + r'\foreach \x in {1, ..., #1} {\filldraw[circopen] (#2*\x, 0) circle [radius=#3 mm];};',
        '\t\t' + r'}',
        '\t' + r'},',
        '\t' + r'pics/skill/.style n args={5}{code={',
        '\t\t' + r'\foreach \x in {1, ..., #1} {\filldraw[circfull] (#4*\x, 0) circle [radius=#5 mm];};',
        '\t\t' + r'\foreach \x in {#2, ..., #3} {\filldraw[circopen] (#4*\x, 0) circle [radius=#5 mm];};',
        '\t\t' + r'}',
        '\t' + r'},',
        r'}',
        ]
    return l


def declare_layers():
    """
    Define pgf layers
    """
    l = [
        r'\pgfdeclarelayer{background}', 
        r'\pgfdeclarelayer{forebackground}', 
        r'\pgfdeclarelayer{foreground}', 
        r'\pgfsetlayers{background, forebackground, main, foreground}',
        ]
    return l


def assemble_letter(dict_letter, letter_text, dict_pers, dict_cont, dict_comp, icons, encl, dict_set):
    """
    Assemble LaTeX code for letter
    """
    letter = geo.Letter(dict_letter)
    # Layout
    l = [
        r'% === LETTER ===',
        r'\begin{tikzpicture}[',
        '\t' + r'inner xsep=0pt,',
        '\t' + r'inner ysep=0pt,',
        '\t' + r']',
        '\t' + r'\begin{pgfonlayer}{background}',
        '\t\t\\fill [fill=none] (0, 0) rectangle ({}, {});'.format(letter.width, letter.height),
        '\t' + r'\end{pgfonlayer}',
        ]
    # Area highlighting
    if letter.highlight is True:
        l2 = [
             '\t' + r'% AREA HIGHLIGHTING',
             '\t' + r'\begin{pgfonlayer}{forebackground}',
             '\t\t' + r'\begin{scope}[',
             '\t\t\t' + 'fill={}, draw={},'.format(letter.highlight_color, 'black'),
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
            '\t' + '\\node [anchor=south west, text width=9cm, align=center, font=\\scriptsize] at ({}, {}) {{{}}};'.format(letter.address_x, letter.backaddress_y, backaddress.oneline('0.6cm', '$\\bullet$'))
            ]
        l = l + l3
    recipient = cv.Company(dict_comp).address()
    # Recipient address
    l.append('\t' + r'% |- Recipient address')
    l.append('\t\\node [anchor=north west, minimum width={0}cm, minimum height=2.73cm, text width={0}cm, align=left] at ({1}, {2}) {{{3}}};'.format(letter.address_width, letter.border_left, letter.backaddress_y, recipient))
    # Headline
    x = letter.width-letter.border_right
    y = letter.height-letter.border_top
    anchor = 'south east'
    size = 'Large'
    headline = '{}~{}~{}'.format(dict_pers['title'], dict_pers['first_name'], dict_pers['family_name'])
    l.append('\t' + r'% |- Headline')
    l.append('\t\\node [anchor={}, align=right, font=\\{}, inner ysep=2pt] at ({}, {}) {{{}}};'.format(anchor, size, x, y, headline))
    l.append('\t' + r'% |- Headline separator')
    l.append('\t' + '\\draw [draw=Blues-K, line width=2.0] ({}, {}) -- +({}, 0);'.format(letter.border_left, y, x-letter.border_left))
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
            '\t\t\t' + r'column 1/.style={nodes={cell1, text width=8.5cm, inner xsep=5pt}},',
            '\t\t\t' + r'column 2/.style={nodes={cell3}},',
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
        email_subject = 'Ihre Bewerbung bei {}'.format(dict_comp['name'])
        l4.append('\t\t\t\\node {{\\href{{mailto:{0}?subject={1}}}{{{0}}}}}; & \\node {{{2}}};\\\\'.format(contact.email, email_subject, icons['mail']))
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
    subject = 'Bewerbung als {}'.format(dict_comp['position'])
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
    closing = 'Mit freundlichen Grüßen,'
    signature = dict_pers['signature']
    l.append('\t' + '\\node (closing) [anchor=north west, text width=10cm, yshift={}cm] at (textbox.south west) {{{}\\\\\\includegraphics[height=1.3cm]{{{}}}\\\\{} {}}};'.format(letter.closing_y_shift, closing, signature, dict_pers['first_name'], dict_pers['family_name']))
    # Enclosure
    l.append('\t' + r'% |- Enclosure')
    enclosure = 'Anlagen:'
    for item in encl:
        enclosure = '{} {},'.format(enclosure, item)
    enclosure = enclosure[:-1]
    l.append('\t\\node [anchor=north west, text width={}cm, yshift={}cm] at (closing.south west) {{{}}};'.format(letter.text_width, letter.enclosure_y_shift, enclosure))
    l.append(r'\end{tikzpicture}')
    return l
 

def assemble_latex(outfile, version_str, config_file_geo, config_file_data, text, microtype, include_meta, encl):
    """
    Read out config values, create objects, and assemble LaTeX code
    """

    def declare_variables():
        """
        Define variables for geometry data
        """
        l = [
            r'\paperw = {}; % paper width'.format(layout.width),
            r'\paperh = {}; % paper height'.format(layout.height),
            ]
        if layout.box_left is True:
            l.append(r'\boxlw = {}; % box left width'.format(box_left.width))
        if layout.box_right is True:
            l.append(r'\boxrw = {}; % box right width'.format(box_right.width))
        if layout.box_top is True:
            l.append(r'\boxth = {}; % box top height'.format(box_top.height))
        if layout.box_bottom is True:
            l.append(r'\boxbh = {}; % box bottom height'.format(box_bottom.height))
        return l


    def draw_background():
        """
        Draw background and boxes
        """
        l = [
            '\t\t' + r'\begin{pgfonlayer}{background}',
            '\t\t\t' + '\\fill[{}] (0, 0) rectangle (\\paperw, \paperh);'.format(layout.background_color),
            '\t\t' + r'\end{pgfonlayer}',
            '\t\t' + r'\begin{pgfonlayer}{forebackground}',
            ]
        if layout.box_left is True:
            l.append('\t\t\t' + '\\fill[{}] (0, 0) rectangle (\\boxlw, \\paperh); % box left'.format(box_left.color))
        if layout.box_right is True:
            l.append('\t\t\t' + '\\fill[{}] ({}, 0) rectangle (\\paperw, \\paperh); % box right'.format(box_right.color, layout.width-box_right.width))
        if layout.box_top is True:
            l.append('\t\t\t' + '\\fill[{}] (0, {}) rectangle (\\paperw, \\paperh); % box top'.format(box_top.color, layout.height-box_top.height))
        if layout.box_bottom is True:
            l.append('\t\t\t' + '\\fill[{}] (0, 0) rectangle (\\paperw, \\boxbh); % box bottom'.format(box_bottom.color))
        l.append('\t\t' + r'\end{pgfonlayer}')
        return l


    # Read config files
    config_data = fn.read_config(config_file_data)
    config_geo = fn.read_config(config_file_geo)
    dict_layout = config_geo['cv']['layout']
    dict_letter = config_geo['letter']
    dict_box = config_geo['cv']['boxes']
    dict_box_top = dict_box['box_top']
    dict_box_bottom = dict_box['box_bottom']
    dict_box_left = dict_box['box_left']
    dict_box_right = dict_box['box_right']
    dict_skill_layout = config_geo['cv']['skills']['layout']
    dict_skill_circle = config_geo['cv']['skills']['circle']
    cv_lang = config_geo['cv']['layout']['language']
    cv_pages = config_geo['cv']['layout']['pages']
    dict_areas = config_geo['cv']['areas']
    structure = config_geo['structure']
    # Create objects
    layout = geo.Layout(dict_layout)
    background_box = geo.Box(color=dict_layout['background_color'], width=dict_layout['width'], height=dict_layout['height'])
    box_top = geo.Box(color=dict_box_top['color'], width=layout.width, height=dict_box_top['size'])
    box_bottom = geo.Box(color=dict_box_bottom['color'], width=layout.width, height=dict_box_bottom['size'])
    box_left = geo.Box(color=dict_box_left['color'], width=dict_box_left['size'], height=layout.height)
    box_right = geo.Box(color=dict_box_right['color'], width=dict_box_right['size'], height=layout.height)

    # General settings
    dict_set = config_geo['general']

    # Icons
    icons = config_geo['icons']
    icon_names = config_data['Contact']['icons']

    # Assemble personal area
    dict_pers = config_data['Personal']
    person = cv.Personal(dict_pers)
    area_personal = geo.Area(dict_areas['personal'])
    x = area_personal.pos_x
    y = area_personal.pos_y
    anchor = area_personal.anchor
    hsize = area_personal.head_font_size
    bsize = area_personal.body_font_size
    pers = [
            '% PERSONAL AREA',
            '% |- Title:',
            ]
    pers.append('\\node (pers) [anchor={}, font=\\{}] at ({}, {}) {{{}}};'.format(anchor, hsize, x, y, area_personal.title))
    pers.append('% |- Items:')
    if area_personal.style == 'oneline':
        about_str = geo.Personal(dict_pers).oneline(cv_lang)
    elif area_personal.style == 'twoline':
        about_str = geo.Personal(dict_pers).twoline(cv_lang)
    pers.append('\\node [below={} of pers.south west, anchor=north west, font=\\{}, align=left] {{{}}};'.format(area_personal.head_vspace, bsize, about_str))

    # Assemble title
    area_title = geo.Area(dict_areas['title'])
    x = area_title.pos_x
    y = area_title.pos_y
    l = area_title.length
    anchor = area_title.anchor
    hsize = area_title.head_font_size
    bsize = area_title.body_font_size
    title = [
            '% TITLE',
            '\\node [anchor={}, font=\\{}] at ({}, {}) {{{} {}}};'.format(anchor, hsize, x, y, person.first_name, person.family_name),
            ]
    if area_title.head_sepline is True:
        title.append('\\draw [draw={}, line width=1pt] ({}, {}) -- ({}, {});'.format(area_title.color, x, y-0.8, l, y-0.8))
    title.append('\\node [anchor={}, font=\\{}, text height=0.6cm] at ({}, {}) {{{}}};'.format(anchor, bsize, x, y-0.8, area_title.title))
 

    # Assemble photo
    dict_photo = config_geo['cv']['areas']['photo']
    photo_file = config_data['Personal']['photo']
    area_photo = geo.PhotoArea(dict_photo)
    x = area_photo.pos_x
    y = area_photo.pos_y
    anchor = area_photo.anchor
    width = area_photo.width
    height = area_photo.height
    if area_photo.border is True:
        border_color = area_photo.border_color
    else:
        border_color = 'none'
    photo = [
            '% PHOTO AREA',
            r'\begin{scope}',
            '\t' + '\\clip  ({}, {}) rectangle ({}, {});'.format(x, y, x+width, y-height),
            '\t\\node[anchor={}, inner sep=0] (image) at ({}, {}) {{\\includegraphics[width={}cm]{{{}}}}};'.format(anchor, x, y, width, photo_file),
            '\t' + '\\draw [draw={}, line width={}] ({}, {}) rectangle ({}, {});'.format(border_color, area_photo.border_width, x, y, x+width, y-height),
            r'\end{scope}',
            ]

    # Assemble contact area
    area_contact = geo.Area(dict_areas['contact'])
    x = area_contact.pos_x
    y = area_contact.pos_y
    anchor = area_contact.anchor
    hsize = area_contact.head_font_size
    bsize = area_contact.body_font_size
    hspace1 = area_contact.body_indent
    vspace1 = area_contact.body_vspace
    cont = [
            '% CONTACT AREA',
            '% |- Title:',
            '\\node (cont) [anchor={}, font=\\{}] at ({}, {}) {{{}}};'.format(anchor, hsize, x, y, area_contact.title),
            '% |- Items:',
            '\\begin{{scope}}[row sep=-\\pgflinewidth, column sep=-\\pgflinewidth, text depth=0.0cm, minimum height=0.5cm, font=\\{}]'.format(bsize),
            '\t\\matrix (con) at ({}, {}) ['.format(x, y-area_contact.head_vspace),
            '\t\t' + 'anchor=north west,'.format(anchor),
            '\t\t' + r'matrix of nodes,',
            '\t\t' + r'column 1/.style={nodes={cell3}},',
            '\t\t' + r'column 2/.style={nodes={cell4}},',
            '\t\t' + r']{',
            ]
    dict_cont = config_data['Contact']
    contact = cv.Contact(dict_cont)
    address_data = geo.Address(dict_cont)
    address = address_data.twoline()
    vspace2 = 0.5
    cont.append('\t\t\\node [text depth={}cm] {{{}}}; & \\node [text depth={}cm] {{{}}};\\\\'.format(vspace2, icons['address'], vspace2, address))
    cont.append('\t\t\\node {{{}}}; & \\node {{{}}};\\\\'.format(icons['phone'], contact.phone))
    cont.append('\t\t\\node {{{}}}; & \\node {{{}}};\\\\'.format(icons['mail'], contact.email))
    cont.append('\t\t\\vspace{1cm} & \\vspace{1cm}\\\\')
    for key, value in contact.weblinks.items():
        if key not in area_contact.hide_items:
            key = key.replace('_', r'\_')
            value = value.replace('_', r'\_')
            if (area_contact.hyperlinks is True) and (value != ''):
                value = r'\href{' + value + r'}{' + value.replace('https://', '').replace('www.', '') + '}'
                if 'linkedin' in value:
                    depth = '0.5cm'
                else:
                    depth = '0.0cm'
            cont.append('\t\t\\node [text depth={}] {{{}}}; & \\node [text depth={}] {{{}}};\\\\'.format(depth, icons[icon_names[key]], depth, value))
    cont.append('\t\t'+ r'};')
    cont.append(r'\end{scope}')
    
    # Read career items
    dict_career = config_data['Career']

    # Assemble career items
    area_career = geo.Area(dict_areas['career'])
    x = area_career.pos_x
    y = area_career.pos_y
    anchor = area_career.anchor
    hsize = area_career.head_font_size
    bsize = area_career.body_font_size
    hspace1 = area_career.body_indent
    vspace1 = area_career.body_vspace
    car = [
            '% CAREER AREA',
            '% |- Title:',
            r'\node [anchor={}, font=\{}] at ({}, {}) {{{}}};'.format(anchor, hsize, x, y, area_career.title),
            '% |- Items:',
            '\\begin{{scope}}[row sep=-\\pgflinewidth, column sep=-\\pgflinewidth, text depth=0.0cm, minimum height=0.5cm, font=\\{}]'.format(bsize),
            '\t\\matrix (edu) at ({}, {}) ['.format(x, y-area_career.head_vspace),
            '\t\t' + 'anchor={},'.format(anchor),
            '\t\t' + r'matrix of nodes,',
            '\t\t' + r'column 1/.style={nodes={cell1}},',
            '\t\t' + r'column 2/.style={nodes={cell2}},',
            '\t\t' + r']{',
            ]

    car_items = []
    for car_item in dict_career.values():
        car_items.append(cv.CareerItem(car_item))
    for car_item in reversed(car_items):
        car.append('\t\t\\node {{{}\\,--\\,{}}}; & \\node {{{}}};\\\\'.format(car_item.start_date, car_item.end_date, car_item.company_name))
        car.append('\t\t & \\node [text depth=0.5cm] {{{}}};\\\\'.format(car_item.description))
    car.append('\t\t' + r'};')
    car.append(r'\end{scope}')

    # Read education items
    dict_edu = config_data['Education']
    edu_items = []
    for edu_item in dict_edu.values():
        if 'start_date' in edu_item:
            edu_items.append(cv.EduPeriodItem(edu_item))
        else:
            edu_items.append(cv.EduEventItem(edu_item))
    # Assemble education items
    area_edu = geo.Area(dict_areas['education'])
    x = area_edu.pos_x
    y = area_edu.pos_y
    anchor = area_edu.anchor
    hsize = area_edu.head_font_size
    bsize = area_edu.body_font_size
    hspace1 = area_edu.body_indent
    vspace1 = area_edu.body_vspace
    edu = [
            '% EDUCATION AREA',
            '% |- Title:',
            r'\node [anchor={}, font=\{}] at ({}, {}) {{{}}};'.format(anchor, hsize, x, y, area_edu.title),
            '% |- Items:',
            '\\begin{{scope}}[row sep=-\\pgflinewidth, column sep=-\\pgflinewidth, text depth=0.0cm, minimum height=0.5cm, font=\{}]'.format(bsize),
            '\t\\matrix (edu) at ({}, {}) ['.format(x, y-area_edu.head_vspace),
            '\t\t' + 'anchor={},'.format(anchor),
            '\t\t' + r'matrix of nodes,',
            '\t\t' + r'column 1/.style={nodes={cell1}},',
            '\t\t' + r'column 2/.style={nodes={cell2}},',
            '\t\t' + r']{',
            ]

    for edu_item in reversed(edu_items):
        if isinstance(edu_item, cv.EduPeriodItem):
            edu.append('\t\t\\node {{{}\\,--\\,{}}}; & \\node {{{}}};\\\\'.format(edu_item.start_date, edu_item.end_date, edu_item.school_name))
            edu.append('\t\t & \\node [text depth=0.5cm] {{{}}};\\\\'.format(edu_item.description))
        else:
            edu.append('\t\t\\node {{{}}}; & \\node {{{}}};\\\\'.format(edu_item.date, edu_item.school_name))
            edu.append('\t\t & \\node [text depth=0.5cm] {{{}}};\\\\'.format(edu_item.description))
    edu.append('\t\t' + r'};')
    edu.append(r'\end{scope}')

    # Read skill items
    dict_skills = config_data['skills']
    skill_objects = []
    for item in dict_skills.values():
        skill_objects.append(cv.SkillItem(item))

    skill_groups = []
    for item in skill_objects:
        skill_groups.append(item.group)  # get all skill groups
    skill_groups = list(set(skill_groups))  # get unique skill groups
    
    skill_circle = geo.SkillCircle(dict_skill_circle)
    skill_layout = geo.SkillLayout(dict_skill_layout)
    num = skill_layout.number
    dist = skill_layout.distance
    rad = skill_circle.radius
    area_skills = geo.Area(dict_areas['skills'])
    x = area_skills.pos_x
    y = area_skills.pos_y
    anchor = area_skills.anchor
    hsize = area_skills.head_font_size
    bsize = area_skills.body_font_size

    # Assemble skills
    skills = [
            '% SKILL AREA',
            '% |- Title:',
            r'\node [anchor={}, font=\{}] at ({}, {}) {{{}}};'.format(anchor, hsize, x, y, area_skills.title),
            '% |- Items:',
            '\\begin{{scope}}[row sep=-\\pgflinewidth, column sep=-\\pgflinewidth, text depth=0.0cm, minimum height=0.5cm, font=\{}]'.format(bsize),
            '\t\\matrix (skills) at ({}, {}) ['.format(x, y-area_skills.head_vspace),
            '\t\t' + 'anchor={},'.format(anchor),
            '\t\t' + r'matrix of nodes,',
            '\t\t' + r'column 1/.style={nodes={cell5}},',
            '\t\t' + r'column 2/.style={nodes={cell6}},',
            '\t\t' + r']{',
            ]
    desc = 0
    descr = []
    for group in skill_groups:
        skills.append('\t\t\\node {{{}}};\\\\'.format(group.replace('&', '\&')))
        for item in skill_objects:
            if item.group == group:
                if item.level == num:
                    skills.append('\t\t\\node {{{}}}; & \\node {{\\tikz{{\\pic {{skillmax={{{}}}{{{}}}{{{}}}}};}}}};\\\\'.format(item.name, num, dist, rad))
                elif item.level == 0:
                    skills.append('\t\t\\node {{{}}}; & \\node {{\\tikz{{\\pic {{skillmin={{{}}}{{{}}}{{{}}}}};}}}};\\\\'.format(item.name, num, dist, rad))
                else:
                    skills.append('\t\t\\node {{{}}}; & \\node {{\\tikz{{\\pic {{skill={{{}}}{{{}}}{{{}}}{{{}}}{{{}}}}};}}}};\\\\'.format(item.name, item.level, item.level+1, num, dist, rad))
                if item.description != '':
                    skills.append('\t\t\\node (d{}) {{}}; & \\node {{}};\\\\'.format(desc))
                    descr.append('\\node [cell7, anchor=north west, font=\{}] at (d{}.north west) {{({})}};'.format(bsize, desc, item.description))
                    desc += 1
        skills.append('\t\t\\node {{{}}};\\\\')
    skills.append('\t\t' + r'};')
    skills.append(r'\end{scope}')
    skills = skills + descr

    # Read knowledge items
    dict_know = config_data['knowledge']
    know_objects = []
    for item in dict_know.values():
        know_objects.append(cv.KnowledgeItem(item))

    know_groups = []
    for item in know_objects:
        know_groups.append(item.group)  # get all groups
    know_groups = list(set(know_groups))  # get unique groups
    
    area_know = geo.Area(dict_areas['knowledge'])
    x = area_know.pos_x
    y = area_know.pos_y
    anchor = area_know.anchor
    hsize = area_know.head_font_size
    bsize = area_know.body_font_size

    # Assemble knowledge
    know = [
            '% KNOWLEDGE AREA',
            '% |- Title:',
            r'\node [anchor={}, font=\{}] at ({}, {}) {{{}}};'.format(anchor, hsize, x, y, area_know.title),
            '% |- Items:',
            '\\begin{{scope}}[row sep=-\\pgflinewidth, column sep=-\\pgflinewidth, text depth=0.0cm, minimum height=0.5cm, font=\{}]'.format(bsize),
            '\t\\matrix (skills) at ({}, {}) ['.format(x, y-area_know.head_vspace),
            '\t\t' + 'anchor={},'.format(anchor),
            '\t\t' + r'matrix of nodes,',
            '\t\t' + r'column 1/.style={nodes={cell5}},',
            '\t\t' + r'column 2/.style={nodes={cell6}},',
            '\t\t' + r']{',
            ]
    for group in know_groups:
        know.append('\t\t\\node {{{}}};\\\\'.format(group.replace('&', '\&')))
        for item in know_objects:
            if item.group == group:
                    know.append('\t\t\\node {{{}}}; & \\node {{{}}};\\\\'.format(item.name, item.description))
        know.append('\t\t\\node {{{}}};\\\\')
    know.append('\t\t' + r'};')
    know.append(r'\end{scope}')

    # Read certificate items
    dict_cert = config_data['certificates']
    cert_objects = []
    for item in dict_cert.values():
        cert_objects.append(cv.CertificateItem(item))

    cert_groups = []
    for item in cert_objects:
        cert_groups.append(item.group)  # get all groups
    cert_groups = list(set(cert_groups))  # get unique groups
    
    area_cert = geo.Area(dict_areas['certificates'])
    x = area_cert.pos_x
    y = area_cert.pos_y
    anchor = area_cert.anchor
    hsize = area_cert.head_font_size
    bsize = area_cert.body_font_size

    # Assemble certificates
    cert = [
            '% CERTIFICATES AREA',
            '% |- Title:',
            r'\node [anchor={}, font=\{}] at ({}, {}) {{{}}};'.format(anchor, hsize, x, y, area_cert.title),
            '% |- Items:',
            '\\begin{{scope}}[row sep=-\\pgflinewidth, column sep=-\\pgflinewidth, text depth=0.0cm, minimum height=0.5cm, font=\{}]'.format(bsize),
            '\t\\matrix (skills) at ({}, {}) ['.format(x, y-area_cert.head_vspace),
            '\t\t' + 'anchor={},'.format(anchor),
            '\t\t' + r'matrix of nodes,',
            '\t\t' + r'column 1/.style={nodes={cell5}},',
            '\t\t' + r'column 2/.style={nodes={cell6}},',
            '\t\t' + r']{',
            ]
    for group in cert_groups:
        cert.append('\t\t\\node {{{}}};\\\\'.format(group.replace('&', '\&')))
        for item in cert_objects:
            if item.group == group:
                if area_cert.hyperlinks is True:
                    value = '\\href{{{}}}{{{}}}'.format(item.name, item.url)
                else:
                    value = item.name
                cert.append('\t\t\\node {{{}}};\\\\'.format(value))
#        cert.append('\t\t\\node {{{}}};\\\\')
    cert.append('\t\t' + r'};')
    cert.append(r'\end{scope}')

    # Metadata
    dict_comp = config_data['company']
    company = cv.Company(dict_comp)
    meta = cv.Metadata(person.first_name, person.family_name, person.title, contact.city, contact.country, contact.email, company.name, company.position, version_str)

    # Insert variables into letter text
    for count, line in enumerate(text):
        text[count] = line.replace('{Company}', company.name).replace('{Position}', company.position)

    # Write to file
    with open(outfile, 'w', encoding='UTF-8') as f:
        # Write comment with program and version info
        f.write('% ===== LaTeX code generated by cvgen v{} =====\n'.format(version_str))
        # Write LaTeX preamble
        for line in preamble(microtype, meta, include_meta):
            f.write(line + '\n')
        f.write(r'\begin{document}' + '\n')
        # Write definitions of variables
        f.write('\t' + r'\tikzmath{' + '\n')
        for line in declare_variables():
            f.write('\t\t' + line + '\n')
        f.write('\t' + r'}' + '\n')
        # Write style definitions
        for line in tikzset():
            f.write('\t' + line + '\n')
        # Write layer declaration
        for line in declare_layers():
            f.write('\t' + line + '\n')
        if structure['letter'] is True:
            # Write letter
            for line in assemble_letter(dict_letter, text, dict_pers, dict_cont, dict_comp, icons, encl, dict_set):
                f.write('\t' + line + '\n')
        if structure['cv'] is True:
            # Write CV
            f.write('\t' + r'% === CURRICULUM VITAE ===' + '\n')
            f.write('\t' + r'\begin{tikzpicture}[' + '\n')
            f.write('\t\t' + r'inner xsep=0pt,' + '\n')
            f.write('\t\t' + r'inner ysep=0pt,' + '\n')
            f.write('\t\t' + r']' + '\n')
            for line in draw_background():
                f.write(line + '\n')
            f.write('\t\t' + r'\begin{pgfonlayer}{foreground}' + '\n')
            for c in cont:
                f.write('\t\t\t' + c + '\n')
            for skill in skills:
                f.write('\t\t\t' + skill + '\n')
            for k in know:
                f.write('\t\t\t' + k + '\n')
            for c in cert:
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
            f.write('\t' + r'\end{tikzpicture}' + '\n')
            if cv_pages > 1:
                f.write('\t' + r'\begin{tikzpicture}[' + '\n')
                f.write('\t\t' + r'inner xsep=0pt,' + '\n')
                f.write('\t\t' + r'inner ysep=0pt,' + '\n')
                f.write('\t\t' + r']' + '\n')
                f.write('\t\t' + '\\fill[fill=none] (0, 0) rectangle ({}, {});\n'.format(layout.width, layout.height))
                f.write('\t' + r'\end{tikzpicture}' + '\n')
        f.write(r'\end{document}' + '\n')

