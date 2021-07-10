#!/usr/bin/env python3

import cvdata as cv
import geometry as geo
import functions as fn
from PyPDF2 import PdfFileMerger


def mergepdfs(pdflist, target):
    merger = PdfFileMerger()
    for pdf in pdflist:
        merger.append(partfile)
    merger.write(target)
    merger.close()


def preamble():
    """
    Define LaTeX preamble with required packages included
    """
    l = [
        r'\documentclass[12pt, tikz, multi, crop]{standalone}',
        r'\usepackage[sfdefault, scaled=1.0098]{FiraSans}',
        r'\usepackage{newtxsf}',
        r'\usepackage{fontawesome5}',
        r'\usepackage{tikz}',
        r'\usepackage{hyperref}',
        r'\usetikzlibrary{positioning, math, colorbrewer, backgrounds, matrix}',
        r'\standaloneenv{tikzpicture}',
        r'\hypersetup{',
        '\t' + r'colorlinks=true,',
        '\t' + r'urlcolor=Blues-J,',
        r'}',
        ]
    return l


def tikzset():
    """
    Define styles
    """
    l = [
        r'\tikzset{',
        '\t' + r'cell1/.style={rectangle, draw=black, inner xsep=0pt, inner ysep=4pt, text height=0.3cm, align=right, minimum width=2.0cm, text width=3.5cm},',
        '\t' + r'cell2/.style={rectangle, draw=black, inner xsep=6pt, inner ysep=4pt, text height=0.3cm, align=left, minimum width=1.5cm, text width=8.0cm},',
        '\t' + r'cell3/.style={rectangle, draw=black, inner xsep=0pt, inner ysep=4pt, text height=0.3cm, align=center, minimum width=0.6cm, text width=0.4cm},',
        '\t' + r'cell4/.style={rectangle, draw=black, inner xsep=3pt, inner ysep=4pt, text height=0.3cm, align=left, minimum width=1.0cm, text width=5.8cm},',
        '\t' + r'cell5/.style={rectangle, draw=black, inner xsep=0pt, inner ysep=4pt, text height=0.3cm, align=left, minimum width=0.6cm, text width=4.5cm},',
        '\t' + r'cell6/.style={rectangle, draw=black, inner xsep=0pt, inner ysep=4pt, text height=0.3cm, align=right, minimum width=1.0cm, text width=2.0cm},',
        '\t' + r'cell7/.style={rectangle, draw=black, inner xsep=0pt, inner ysep=4pt, text height=0.3cm, align=left, minimum width=1.0cm, text width=6.5cm},',
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


def assemble_latex(outfile, version_str, config_file_geo, config_file_data):
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
    # Create area objects
#    area_education = geo.Area(dict_areas['timeline'])
    # Create objects
    layout = geo.Layout(dict_layout)
    background_box = geo.Box(color=dict_layout['background_color'], width=dict_layout['width'], height=dict_layout['height'])
    box_top = geo.Box(color=dict_box_top['color'], width=layout.width, height=dict_box_top['size'])
    box_bottom = geo.Box(color=dict_box_bottom['color'], width=layout.width, height=dict_box_bottom['size'])
    box_left = geo.Box(color=dict_box_left['color'], width=dict_box_left['size'], height=layout.height)
    box_right = geo.Box(color=dict_box_right['color'], width=dict_box_right['size'], height=layout.height)

    # Icons
    icons = config_geo['icons']
    icon_names = config_data['Contact']['icons']

    # Assemble personal area
    person = cv.Personal(config_data['Personal'])
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
        about_str = geo.Personal(config_data['Personal']).oneline(cv_lang)
    elif area_personal.style == 'twoline':
        about_str = geo.Personal(config_data['Personal']).twoline(cv_lang)
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
    contact = cv.Contact(config_data['Contact'])
    address_data = geo.Address(config_data['Contact'])
    address = address_data.twoline()
#    address = address_data.oneline()
    vspace2 = 0.5
    cont.append('\t\t\\node [text depth={}cm] {{{}}}; & \\node [text depth={}cm] {{{}}};\\\\'.format(vspace2, icons['address'], vspace2, address))
    cont.append('\t\t\\node {{{}}}; & \\node {{{}}};\\\\'.format(icons['phone'], config_data['Contact']['phone']))
    cont.append('\t\t\\node {{{}}}; & \\node {{{}}};\\\\'.format(icons['mail'], config_data['Contact']['email']))
    cont.append('\t\t\\vspace{1cm} & \\vspace{1cm}\\\\')
    for key, value in config_data['Contact']['weblinks'].items():
        if key not in area_contact.hide_items:
            key = key.replace('_', r'\_')
            value = value.replace('_', r'\_')
            if (area_contact.hyperlinks is True) and (value != ''):
                value = r'\href{' + value + r'}{' + value.replace('https://', '').replace('www.', '') + '}'
                if 'linkedin' in value:
                    depth = '0.5cm'
                else:
                    depth = '0.0cm'
#                value = r'\href{' + value + r'}{' + key + '}'
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

    # Assemble skills
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


    # Write to file
    with open(outfile, 'w', encoding='UTF-8') as f:
        # Write comment with program and version info
        f.write('% ===== LaTeX code generated by cvgen v{} =====\n'.format(version_str))
        # Write LaTeX preamble
        for line in preamble():
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
        for p in pers:
            f.write('\t\t\t' + p + '\n')
        for i in photo:
            f.write('\t\t\t' + i + '\n')
        for t in title:
            f.write('\t\t\t' + t + '\n')
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

