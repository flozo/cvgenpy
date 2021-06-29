#!/usr/bin/env python3

import cvdata as cv
import geometry as geo
import functions as fn

def preamble():
    """
    Define LaTeX preamble with required packages included
    """
    l = [
        r'\documentclass[12pt, tikz]{standalone}',
        r'\usepackage[sfdefault, scaled=1.0098]{FiraSans}',
        r'\usepackage{newtxsf}',
        r'\usepackage{tikz}',
        r'\usetikzlibrary{positioning, math, colorbrewer, backgrounds}',
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


def declare_variables(layout, config_geo):
    """
    Define variables for geometry data
    """
#    layout = geo.split_config(config_geo)[0]
    l = [
        r'\paperh = {}; % paper height'.format(layout.height),
        r'\paperw = {}; % paper width'.format(layout.width),
        ]
    if layout.box_top is True:
        box_top = geo.split_config(config_geo)[1]
        l.append(r'\boxth = {}; % box top height'.format(box_top.height))
    if layout.box_bottom is True:
        box_bottom = geo.split_config(config_geo)[2]
        l.append(r'\boxbh = {}; % box bottom height'.format(box_bottom.height))
    if layout.box_left is True:
        box_left = geo.split_config(config_geo)[3]
        l.append(r'\boxlw = {}; % box left width'.format(box_left.width))
    if layout.box_right is True:
        box_right = geo.split_config(config_geo)[4]
        l.append(r'\boxrw = {}; % box right width'.format(box_right.width))
#    if cv.skills.layout.show_circles is True:
#        l.append('\t\tikzset{')
#        l.append('\t\t' + r'skillbar/.pic={')
#        l.append('\t\t\t' + r'\path')
#        l.append('\t\t\t' + r'(0, 0) coordinate (-A1)')
#        l.append('\t\t\t' + r'(\x1, 0) coordinate (-A2)')
#        for i in range(2, cv.skills.layout.circle_number + 1):
#            l.append('\t\t\t' + '(\\x1*{}, 0) coordinate (-A{})'.format(i, i+1))
    return l


def draw_background(layout, config_geo):
    """
    Draw background and boxes
    """
    if layout.box_top is True:
        box_top = geo.split_config(config_geo)[1]
    if layout.box_bottom is True:
        box_bottom = geo.split_config(config_geo)[2]
    if layout.box_left is True:
        box_left = geo.split_config(config_geo)[3]
    if layout.box_right is True:
        box_right = geo.split_config(config_geo)[4]
    l = [
        '\t\t' + r'\begin{pgfonlayer}{background}',
        '\t\t\t' + '\\fill[{}] (0, 0) rectangle ({}, {});'.format(layout.background_color, layout.width, layout.height),
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


def assemble_latex(outfile, version_str, config_file_geo, config_file_data):
    """
    Read out config values, create objects, and assemble LaTeX code
    """
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

    # Read education items
    dict_edu = config_data['Education']
    edu_items = []
    for edu_item in dict_edu.values():
        edu_items.append(cv.EduItem(edu_item))
    # Assemble education items
    itemx = 10
    itemy = 15
    hspace1 = 0.5
    vspace1 = 0.1
    indent1 = 1
    edu = ['% Education items']
    for idx, edu_item in enumerate(edu_items):
        print(edu_item.caption)
        edu.append('\\node (eduitem{}) [anchor=mid] at ({}, {}) {{{}\\,--\\,{}}}'.format(idx, itemx, itemy+2*idx, edu_item.beginning, edu_item.end))
        edu.append('\\node (subeduitem{}) [anchor=mid, right={} of eduitem{}.east] {{{}, {}}}'.format(idx, hspace1, idx, edu_item.caption, edu_item.location))
        edu.append('\\node [below={} of subeduitem{}.south west, anchor=north west] {{{}}}'.format(vspace1, idx, edu_item.description))
    print(edu)
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
        for line in declare_variables(layout, config_geo):
            f.write('\t\t' + line + '\n')
        f.write('\t' + r'}' + '\n')
        # Write layer declaration
        for line in declare_layers():
            f.write('\t' + line + '\n')
        f.write('\t' + r'\begin{tikzpicture}[' + '\n')
        f.write('\t\t' + r'inner xsep=0pt,' + '\n')
        f.write('\t\t' + r'inner ysep=0pt,' + '\n')
        f.write('\t\t' + r']' + '\n')
        for line in draw_background(layout, config_geo):
            f.write(line + '\n')
        f.write('\t\t' + r'\begin{pgfonlayer}{foreground}' + '\n')
        for skill in skills:
            f.write('\t\t\t'+ skill + ';\n')
        for edu_item in edu:
            f.write('\t\t\t'+ edu_item + ';\n')
        f.write('\t\t' + r'\end{pgfonlayer}' + '\n')
        f.write('\t' + r'\end{tikzpicture}' + '\n')
        f.write(r'\end{document}' + '\n')

