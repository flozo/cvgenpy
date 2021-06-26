#!/usr/bin/env python3
#
# cvgen v0.3 2021-06-26

# Import modules

import argparse
import cvdata as cv
import geometry as geo
#import time
#import numpy as np

# Version
version_num = '0.3'
version_dat = '2021-06-26'
version_str = '{} ({})'.format(version_num, version_dat)

def main():
    # Define argument parsers and subparsers
    parser = argparse.ArgumentParser(description='A program for generating CVs in LaTeX. Written by Johannes Engelmayer')

    parser.add_argument('-V', '--version', action='version', version='%(prog)s '+ version_str)
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='verbosity level (-v, -vv, -vvv): '
                        'default = single-line output, v = multi-line, vv = detailed, vvv = array output')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help=('disable terminal output (terminates all verbosity)'))
    parser.add_argument('outfile', nargs='?', help='write to file')

    args = parser.parse_args()

    # Check verbosity level

    verbosity = args.verbose
    if args.quiet is True:
        verbosity = -1
    if verbosity >= 1:
        print(args)

    Person1 = cv.Personal(first_name='John', second_name='Peter', hide_second_name=True, family_name='Doe', birth_date='01.02.1989', birth_location='City', married=False, children=0)
    print(Person1)
    print(Person1.birth_location)
    height = 29.7
    width = 21.0
    color_background = 'Blues-G'
    layout = geo.Layout(height, width, color_background, box_top=False, box_bottom=False, box_left=True, box_right=False)
    skill_decoration = True
    # Skill layout
    skill_circle = geo.SkillCircle(radius=2, fillcolor='Reds-E', linecolor='', showline=False)
    skill_layout = geo.SkillLayout(skill_circle, number=5, distance=5)
    # Skill items
    skill1 = cv.SkillItem(name='Python', level=4)
    skill2 = cv.SkillItem(name='Bash', level=3)
    skill3 = cv.SkillItem(name='LaTeX', level=5)
    skill4 = cv.SkillItem(name='Git', level=5)
    # Skill groups
    group1 = cv.SkillGroup(name='Programming', skill_items=[skill1, skill2, skill3])
    group2 = cv.SkillGroup(name='Software/Tools', skill_items=[skill4])
    skills = []
    for i in range(skill_layout.number):
        skills.append('\\filldraw[color={}] ({}, {}) circle [radius={}mm]'.format(skill_circle.fillcolor, 2+i*skill_layout.distance/10, 5, skill_circle.radius))
    print(skills)

    #position = 'top'

    if layout.box_top is True:
        box_top = geo.Box(height=layout.height/6, width=layout.width, color='Greys-J')
    if layout.box_bottom is True:
        box_bottom = geo.Box(height=layout.height/6, width=layout.width, color='Greys-J')
    if layout.box_left is True:
        box_left = geo.Box(height=layout.height, width=layout.width/7, color='Greys-J')
    if layout.box_right is True:
        box_right = geo.Box(height=layout.height, width=layout.width/7, color='Greys-J')

    # Check file extension
    outfile = str(args.outfile)
    if outfile[-4:0] != '.tex':
        outfile = outfile + '.tex'
    # Write to file
    with open(outfile, 'w', encoding='UTF-8') as f:
        f.write('% ===== LaTeX code generated by cvgen v{} =====\n'.format(version_str))
        f.write(r'\documentclass[12pt, tikz]{standalone}' + '\n')
        f.write(r'\usepackage[sfdefault, scaled=1.0098]{FiraSans}' + '\n')
        f.write(r'\usepackage{newtxsf}' + '\n')
        f.write(r'\usepackage{tikz}' + '\n')
        f.write(r'\usetikzlibrary{positioning, colorbrewer, backgrounds}' + '\n')
        f.write(r'\begin{document}' + '\n')
        f.write('\t' + r'\pgfdeclarelayer{background}' + '\n')
        f.write('\t' + r'\pgfdeclarelayer{forebackground}' + '\n')
        f.write('\t' + r'\pgfdeclarelayer{foreground}' + '\n')
        f.write('\t' + r'\pgfsetlayers{background, forebackground, main, foreground}' + '\n')
        f.write('\t' + r'\begin{tikzpicture}' + '\n')
        f.write('\t\t' + r'\begin{pgfonlayer}{background}' + '\n')
        f.write('\t\t\t' + '\\fill[{}] (0, 0) rectangle ({}, {});\n'.format(layout.color, layout.width, layout.height))
        f.write('\t\t' + r'\end{pgfonlayer}' + '\n')
        f.write('\t\t' + r'\begin{pgfonlayer}{forebackground}' + '\n')
        if layout.box_top is True:
            f.write('\t\t\t' + '\\fill[{}] (0, {}) rectangle ({}, {});\n'.format(box_top.color, layout.height-box_top.height, box_top.width, layout.height))
        if layout.box_bottom is True:
            f.write('\t\t\t' + '\\fill[{}] (0, 0) rectangle ({}, {});\n'.format(box_bottom.color, box_bottom.width, box_bottom.height))
        if layout.box_left is True:
            f.write('\t\t\t' + '\\fill[{}] (0, 0) rectangle ({}, {});\n'.format(box_left.color, box_left.width, layout.height))
        if layout.box_right is True:
            f.write('\t\t\t' + '\\fill[{}] ({}, 0) rectangle ({}, {});\n'.format(box_right.color, layout.width-box_right.width, layout.width, layout.height))
        f.write('\t\t' + r'\end{pgfonlayer}' + '\n')
        if skill_decoration is True:
            f.write('\t\t' + r'\begin{pgfonlayer}{foreground}' + '\n')
            for i in range(skill_layout.number):
                f.write('\t\t\t'+ skills[i] + ';\n')
            f.write('\t\t' + r'\end{pgfonlayer}' + '\n')
        f.write('\t' + r'\end{tikzpicture}' + '\n')
        f.write(r'\end{document}' + '\n')

if __name__ == '__main__':
    main()
