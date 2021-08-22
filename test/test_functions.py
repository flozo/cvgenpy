#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 18:57:05 2021

@author: flozo
"""

import cvgen.functions as fn
import pandas as pd


def test_make_section_header_left():
    """Test function for make_section_header_left."""
    data_initial = {
        'group': ['Test group', 'Test group', 'Test group', 'Test group'],
        'name': ['Name1', 'Name2', 'Name3', 'Name4'],
        'xyz': ['123', '456', '789', 'abc'],
        }
    data_final = {
        'group': ['Test group', '', '', ''],
        'name': ['Name1', 'Name2', 'Name3', 'Name4'],
        'xyz': ['123', '456', '789', 'abc'],
        }
    dfi = pd.DataFrame(data_initial)
    dff = pd.DataFrame(data_final)
    shl = fn.make_section_header_left(dfi)
    assert shl.equals(dff)


def test_make_section_header_top():
    """Test function for make_section_header_top."""
    data_initial = {
        'group': ['Test group', 'Test group', 'Test group', 'Test group'],
        'name': ['Name1', 'Name2', 'Name3', 'Name4'],
        'xyz': ['123', '456', '789', 'abc'],
        }
    data_final = {
        'group': ['Test group', '', '', ''],
        'name': ['Name1', 'Name2', 'Name3', 'Name4'],
        'xyz': ['123', '456', '789', 'abc'],
        }
    dfi = pd.DataFrame(data_initial)
    dff = pd.DataFrame(data_final)
    sht = fn.make_section_header_left(dfi)
    assert sht.equals(dff)
