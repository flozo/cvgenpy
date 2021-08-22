#!/usr/bin/env python3

from cvgen import geometry as geo


def test_generate():
    items = ['item1', 'item2', 'item3', 'item4']
    list_row_comma = geo.List(items, separator=', ', orientation='row')
    list_column_comma = geo.List(items, separator=',', orientation='column')
    assert list_row_comma.generate() == 'item1, item2, item3, item4'
    assert list_column_comma.generate() == 'item1,\\\\item2,\\\\item3,\\\\item4'
