#!/usr/bin/env python3

import cvdata as cv
import geometry as geo

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

