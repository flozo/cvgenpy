#!/usr/bin/env python3

import cvdata as cv
import geometry as geo
import functions as fn


def preamble():
    """
    Define LaTeX preamble with required packages included
    """
    l = [
        r'\documentclass[12pt, tikz, multi, crop]{standalone}',
        r'\usepackage[sfdefault, scaled=1.0098]{FiraSans}',
        r'\usepackage{newtxsf}',
        r'\usepackage{tikz}',
        r'\usetikzlibrary{positioning, math, colorbrewer, backgrounds, matrix}',
        r'\standaloneenv{tikzpicture}',
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
        if layout.box_top is True:
            l.append(r'\boxth = {}; % box top height'.format(box_top.height))
        if layout.box_bottom is True:
            l.append(r'\boxbh = {}; % box bottom height'.format(box_bottom.height))
        if layout.box_left is True:
            l.append(r'\boxlw = {}; % box left width'.format(box_left.width))
        if layout.box_right is True:
            l.append(r'\boxrw = {}; % box right width'.format(box_right.width))
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
        if layout.box_top is True:
            l.append('\t\t\t' + '\\fill[{}] (0, {}) rectangle (\\paperw, \\paperh); % box top'.format(box_top.color, layout.height-box_top.height))
        if layout.box_bottom is True:
            l.append('\t\t\t' + '\\fill[{}] (0, 0) rectangle (\\paperw, \\boxbh); % box bottom'.format(box_bottom.color))
        if layout.box_left is True:
            l.append('\t\t\t' + '\\fill[{}] (0, 0) rectangle (\\boxlw, \\paperh); % box left'.format(box_left.color))
        if layout.box_right is True:
            l.append('\t\t\t' + '\\fill[{}] ({}, 0) rectangle (\\paperw, \\paperh); % box right'.format(box_right.color, layout.width-box_right.width))
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
    area_personal = geo.Area(dict_areas['personal'])
    area_contact = geo.Area(dict_areas['contact'])
#    area_education = geo.Area(dict_areas['timeline'])
    # Create objects
    layout = geo.Layout(dict_layout)
    background_box = geo.Box(color=dict_layout['background_color'], width=dict_layout['width'], height=dict_layout['height'])
    box_top = geo.Box(color=dict_box_top['color'], width=layout.width, height=dict_box_top['size'])
    box_bottom = geo.Box(color=dict_box_bottom['color'], width=layout.width, height=dict_box_bottom['size'])
    box_left = geo.Box(color=dict_box_left['color'], width=dict_box_left['size'], height=layout.height)
    box_right = geo.Box(color=dict_box_right['color'], width=dict_box_right['size'], height=layout.height)
    # Assemble personal area
    person = cv.Personal(config_data['Personal'])
    pers = [
            '% PERSONAL AREA',
            '% |- Title:',
            ]
    pers.append('\\node (pers) [anchor=north west, font=\large] at ({}, {}) {{{}}};'.format(area_personal.pos_x, area_personal.pos_y, area_personal.title))
    pers.append('% |- Items:')
    if area_personal.style == 'oneline':
        if cv_lang == 'en':
            about_str = 'Born {} in {}, {}, {} children'.format(person.birth_date, person.birth_location_city, person.marital_status, person.children)
        if cv_lang == 'de':
            about_str = 'Geboren am {} in {}, {}, {} Kinder'.format(person.birth_date, person.birth_location_city, person.marital_status, person.children)
    pers.append('\\node [below={} of pers.south west, anchor=north west, font=\small] {{{}}};'.format(area_personal.head_vspace, about_str))
    # Read career items
    dict_career = config_data['Career']
    print(dict_career)

    # Assemble career items
    area_career = geo.Area(dict_areas['career'])
    itemx = area_career.pos_x
    itemy = area_career.pos_y
    hspace1 = area_career.body_indent
    vspace1 = area_career.body_vspace
    car = [
            '% CAREER AREA',
            '% |- Title:',
            r'\node [anchor=north west, font=\large] at ({}, {}) {{{}}};'.format(itemx, itemy, area_career.title),
            '% |- Items:',
            r'\begin{scope}[row sep=-\pgflinewidth, column sep=-\pgflinewidth, text depth=0.0cm, minimum height=0.5cm]',
            '\t\\matrix (edu) at ({}, {}) ['.format(itemx, itemy-area_career.head_vspace),
            '\t\t' + r'anchor=north west,',
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
        print(edu_item)
        if 'start_date' in edu_item:
            edu_items.append(cv.EduPeriodItem(edu_item))
        else:
            edu_items.append(cv.EduEventItem(edu_item))
    # Assemble education items
    area_edu = geo.Area(dict_areas['education'])
    itemx = area_edu.pos_x
    itemy = area_edu.pos_y
    hspace1 = area_edu.body_indent
    vspace1 = area_edu.body_vspace
    edu = [
            '% EDUCATION AREA',
            '% |- Title:',
            r'\node [anchor=north west, font=\large] at ({}, {}) {{{}}};'.format(itemx, itemy, area_edu.title),
            '% |- Items:',
            r'\begin{scope}[row sep=-\pgflinewidth, column sep=-\pgflinewidth, text depth=0.0cm, minimum height=0.5cm]',
            '\t\\matrix (edu) at ({}, {}) ['.format(itemx, itemy-area_edu.head_vspace),
            '\t\t' + r'anchor=north west,',
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
    skill_circle = geo.SkillCircle(dict_skill_circle)
    skill_layout = geo.SkillLayout(dict_skill_layout)
    # Assemble skills
    skills = []
    for i in range(skill_layout.number):
        skills.append('\\filldraw[color={}] ({}, {}) circle [radius={}mm]'.format(skill_circle.fillcolor, 2+i*skill_layout.distance/10, 5, skill_circle.radius))

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
        # Write layer declaration
        for line in declare_layers():
            f.write('\t' + line + '\n')
        f.write('\t' + r'\begin{tikzpicture}[' + '\n')
        f.write('\t\t' + r'inner xsep=0pt,' + '\n')
        f.write('\t\t' + r'inner ysep=0pt,' + '\n')
        f.write('\t\t' + r'cell1/.style={rectangle, draw=black, inner xsep=0pt, inner ysep=4pt, text height=0.3cm, align=right, minimum width=2.0cm, text width=3.5cm},' + '\n')
        f.write('\t\t' + r'cell2/.style={rectangle, draw=black, inner xsep=6pt, inner ysep=4pt, text height=0.3cm, align=left, minimum width=1.5cm, text width=8.0cm},' + '\n')
        f.write('\t\t' + r']' + '\n')
        for line in draw_background():
            f.write(line + '\n')
        f.write('\t\t' + r'\begin{pgfonlayer}{foreground}' + '\n')
        for skill in skills:
            f.write('\t\t\t' + skill + ';\n')
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

