# test_eng.py
# Copyright (c) 2013-2016 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0103,C0111,C0302,R0915,W0212

# Standard library imports
import sys
import numpy
import pytest
# Putil imports
import putil.test
import putil.eng


###
# Test functions
###
def test_split_every():
    """ Test _split_every function behavior """
    obj = putil.eng._split_every
    assert obj('a, b, c, d', ',', 1) == ['a', ' b', ' c', ' d']
    assert obj('a , b , c , d ', ',', 1) == ['a ', ' b ', ' c ', ' d ']
    assert (
        obj('a , b , c , d ', ',', 1, lstrip=True)
        ==
        ['a ', 'b ', 'c ', 'd ']
    )
    assert (
        obj('a , b , c , d ', ',', 1, rstrip=True)
        ==
        ['a', ' b', ' c', ' d']
    )
    assert (
        obj('a , b , c , d ', ',', 1, lstrip=True, rstrip=True)
        ==
        ['a', 'b', 'c', 'd']
    )
    assert obj('a, b, c, d', ',', 2) == ['a, b', ' c, d']
    assert obj('a, b, c, d', ',', 3) == ['a, b, c', ' d']
    assert obj('a, b, c, d', ',', 4) == ['a, b, c, d']
    assert obj('a, b, c, d', ',', 5) == ['a, b, c, d']


def test_to_sci_string():
    """ Test _to_eng_string function behavior """
    # Positive
    obj = putil.eng._to_sci_string
    assert obj(0.000000000000000000000001001234567890) == '1.00123456789E-24'
    assert obj(0.000000000000000000000001) == '1E-24'
    assert obj(0.00000000000000000000001001234567890) == '10.0123456789E-24'
    assert obj(0.00000000000000000000001) == '10E-24'
    assert obj(0.0000000000000000000001001234567890) == '100.123456789E-24'
    assert obj(0.0000000000000000000001) == '100E-24'
    assert obj(0.000000000000000000001001234567890) == '1.00123456789E-21'
    assert obj(0.000000000000000000001) == '1E-21'
    assert obj(0.00000000000000000001001234567890) == '10.0123456789E-21'
    assert obj(0.00000000000000000001) == '10E-21'
    assert obj(0.0000000000000000001001234567890) == '100.123456789E-21'
    assert obj(0.0000000000000000001) == '100E-21'
    assert obj(0.000000000000000001001234567890) == '1.00123456789E-18'
    assert obj(0.000000000000000001) == '1E-18'
    assert obj(0.00000000000000001001234567890) == '10.0123456789E-18'
    assert obj(0.00000000000000001) == '10E-18'
    assert obj(0.0000000000000001001234567890) == '100.123456789E-18'
    assert obj(0.0000000000000001) == '100E-18'
    assert obj(0.000000000000001001234567890) == '1.00123456789E-15'
    assert obj(0.000000000000001) == '1E-15'
    assert obj(0.00000000000001001234567890) == '10.0123456789E-15'
    assert obj(0.00000000000001) == '10E-15'
    assert obj(0.0000000000001001234567890) == '100.123456789E-15'
    assert obj(0.0000000000001) == '100E-15'
    assert obj(0.000000000001001234567890) == '1.00123456789E-12'
    assert obj(0.000000000001) == '1E-12'
    assert obj(0.00000000001001234567890) == '10.0123456789E-12'
    assert obj(0.00000000001) == '10E-12'
    assert obj(0.0000000001001234567890) == '100.123456789E-12'
    assert obj(0.0000000001) == '100E-12'
    assert obj(0.000000001001234567890) == '1.00123456789E-9'
    assert obj(0.000000001) == '1E-9'
    assert obj(0.00000001001234567890) == '10.0123456789E-9'
    assert obj(0.00000001) == '10E-9'
    assert obj(0.0000001001234567890) == '100.123456789E-9'
    assert obj(0.0000001) == '100E-9'
    assert obj(0.000001001234567890) == '1.00123456789E-6'
    assert obj(0.000001) == '1E-6'
    assert obj(0.00001001234567890) == '10.0123456789E-6'
    assert obj(0.00001) == '10E-6'
    assert obj(0.0001001234567890) == '100.123456789E-6'
    assert obj(0.0001) == '100E-6'
    assert obj(0.001001234567890) == '1.00123456789E-3'
    assert obj(0.001) == '1E-3'
    assert obj(0.01001234567890) == '10.0123456789E-3'
    assert obj(0.01) == '10E-3'
    assert obj(0.1001234567890) == '100.123456789E-3'
    assert obj(0.1) == '100E-3'
    assert obj(0) == '0E+0'
    assert obj(1) == '1E+0'
    assert obj(1.1234567890) == '1.123456789E+0'
    assert obj(10) == '10E+0'
    assert obj(10.1234567890) == '10.123456789E+0'
    assert obj(100) == '100E+0'
    assert obj(100.1234567890) == '100.123456789E+0'
    assert obj(1000) == '1E+3'
    assert obj(1000.1234567890) == (
        '1.00012345679E+3'
        if sys.hexversion < 0x03000000 else
        '1.000123456789E+3'
    )
    assert obj(10000) == '10E+3'
    assert obj(10000.1234567890) == (
        '10.0001234568E+3'
        if sys.hexversion < 0x03000000 else
        '10.000123456789E+3'
    )
    assert obj(100000) == '100E+3'
    assert obj(100000.1234567890) == (
        '100.000123457E+3'
        if sys.hexversion < 0x03000000 else
        '100.000123456789E+3'
    )
    assert obj(1000000) == '1E+6'
    assert obj(1000000.1234567890) == (
        '1.00000012346E+6'
        if sys.hexversion < 0x03000000 else
        '1.000000123456789E+6'
    )
    assert obj(10000000) == '10E+6'
    assert obj(10000000.1234567890) == (
        '10.0000001235E+6'
        if sys.hexversion < 0x03000000 else
        '10.00000012345679E+6'
    )
    assert obj(100000000) == '100E+6'
    assert obj(100000000.1234567890) == (
        '100.000000123E+6'
        if sys.hexversion < 0x03000000 else
        '100.00000012345679E+6'
    )
    assert obj(1000000000) == '1E+9'
    assert obj(1000000000.1234567890) == (
        '1.00000000012E+9'
        if sys.hexversion < 0x03000000 else
        '1.0000000001234568E+9'
    )
    assert obj(10000000000) == '10E+9'
    assert obj(10000000000.1234567890) == (
        '10.0000000001E+9'
        if sys.hexversion < 0x03000000 else
        '10.000000000123457E+9'
    )
    assert obj(100000000000) == '100E+9'
    assert obj(100000000000.1234567890) == (
        '100E+9'
        if sys.hexversion < 0x03000000 else
        '100.00000000012346E+9'
    )
    assert obj(1000000000000) == '1E+12'
    assert obj(1000000000000.1234567890) == (
        '1E+12'
        if sys.hexversion < 0x03000000 else
        '1.0000000000001234E+12'
    )
    assert obj(10000000000000) == '10E+12'
    assert obj(10000000000000.1234567890) == (
        '10E+12'
        if sys.hexversion < 0x03000000 else
        '10.000000000000123E+12'
    )
    assert obj(100000000000000) == '100E+12'
    assert obj(100000000000000.1234567890) == (
        '100E+12'
        if sys.hexversion < 0x03000000 else
        '100.00000000000012E+12'
    )
    assert obj(1000000000000000) == '1E+15'
    assert obj(1000000000000000.1234567890) == (
        '1E+15'
        if sys.hexversion < 0x03000000 else
        '1.0000000000000001E+15'
    )
    assert obj(10000000000000000) == '10E+15'
    assert obj(10000000000000000.1234567890) == '10E+15'
    assert obj(100000000000000000) == '100E+15'
    assert obj(100000000000000000.1234567890) == '100E+15'
    assert obj(1000000000000000000) == '1E+18'
    assert obj(1000000000000000000.1234567890) == '1E+18'
    assert obj(10000000000000000000) == '10E+18'
    assert obj(10000000000000000000.1234567890) == '10E+18'
    assert obj(100000000000000000000) == '100E+18'
    assert obj(100000000000000000000.1234567890) == '100E+18'
    assert obj(1000000000000000000000) == '1E+21'
    assert obj(1000000000000000000000.1234567890) == '1E+21'
    assert obj(10000000000000000000000) == '10E+21'
    assert obj(10000000000000000000000.1234567890) == '10E+21'
    assert obj(100000000000000000000000) == '100E+21'
    assert obj(100000000000000000000000.1234567890) == (
        '100E+21'
        if sys.hexversion < 0x03000000 else
        '100.00000000000001E+21'
    )
    assert obj(1000000000000000000000000) == '1E+24'
    assert obj(1000000000000000000000000.1234567890) == '1E+24'
    assert obj(10000000000000000000000000) == '10E+24'
    assert obj(10000000000000000000000000.1234567890) == '10E+24'
    assert obj(100000000000000000000000000) == '100E+24'
    assert obj(100000000000000000000000000.1234567890) == '100E+24'
    # Negative
    assert obj(-0.000000000000000000000001001234567890) == '-1.00123456789E-24'
    assert obj(-0.000000000000000000000001) == '-1E-24'
    assert obj(-0.00000000000000000000001001234567890) == '-10.0123456789E-24'
    assert obj(-0.00000000000000000000001) == '-10E-24'
    assert obj(-0.0000000000000000000001001234567890) == '-100.123456789E-24'
    assert obj(-0.0000000000000000000001) == '-100E-24'
    assert obj(-0.000000000000000000001001234567890) == '-1.00123456789E-21'
    assert obj(-0.000000000000000000001) == '-1E-21'
    assert obj(-0.00000000000000000001001234567890) == '-10.0123456789E-21'
    assert obj(-0.00000000000000000001) == '-10E-21'
    assert obj(-0.0000000000000000001001234567890) == '-100.123456789E-21'
    assert obj(-0.0000000000000000001) == '-100E-21'
    assert obj(-0.000000000000000001001234567890) == '-1.00123456789E-18'
    assert obj(-0.000000000000000001) == '-1E-18'
    assert obj(-0.00000000000000001001234567890) == '-10.0123456789E-18'
    assert obj(-0.00000000000000001) == '-10E-18'
    assert obj(-0.0000000000000001001234567890) == '-100.123456789E-18'
    assert obj(-0.0000000000000001) == '-100E-18'
    assert obj(-0.000000000000001001234567890) == '-1.00123456789E-15'
    assert obj(-0.000000000000001) == '-1E-15'
    assert obj(-0.00000000000001001234567890) == '-10.0123456789E-15'
    assert obj(-0.00000000000001) == '-10E-15'
    assert obj(-0.0000000000001001234567890) == '-100.123456789E-15'
    assert obj(-0.0000000000001) == '-100E-15'
    assert obj(-0.000000000001001234567890) == '-1.00123456789E-12'
    assert obj(-0.000000000001) == '-1E-12'
    assert obj(-0.00000000001001234567890) == '-10.0123456789E-12'
    assert obj(-0.00000000001) == '-10E-12'
    assert obj(-0.0000000001001234567890) == '-100.123456789E-12'
    assert obj(-0.0000000001) == '-100E-12'
    assert obj(-0.000000001001234567890) == '-1.00123456789E-9'
    assert obj(-0.000000001) == '-1E-9'
    assert obj(-0.00000001001234567890) == '-10.0123456789E-9'
    assert obj(-0.00000001) == '-10E-9'
    assert obj(-0.0000001001234567890) == '-100.123456789E-9'
    assert obj(-0.0000001) == '-100E-9'
    assert obj(-0.000001001234567890) == '-1.00123456789E-6'
    assert obj(-0.000001) == '-1E-6'
    assert obj(-0.00001001234567890) == '-10.0123456789E-6'
    assert obj(-0.00001) == '-10E-6'
    assert obj(-0.0001001234567890) == '-100.123456789E-6'
    assert obj(-0.0001) == '-100E-6'
    assert obj(-0.001001234567890) == '-1.00123456789E-3'
    assert obj(-0.001) == '-1E-3'
    assert obj(-0.01001234567890) == '-10.0123456789E-3'
    assert obj(-0.01) == '-10E-3'
    assert obj(-0.1001234567890) == '-100.123456789E-3'
    assert obj(-0.1) == '-100E-3'
    assert obj(-1) == '-1E+0'
    assert obj(-1.1234567890) == '-1.123456789E+0'
    assert obj(-10) == '-10E+0'
    assert obj(-10.1234567890) == '-10.123456789E+0'
    assert obj(-100) == '-100E+0'
    assert obj(-100.1234567890) == '-100.123456789E+0'
    assert obj(-1000) == '-1E+3'
    assert obj(-1000.1234567890) == (
        '-1.00012345679E+3'
        if sys.hexversion < 0x03000000 else
        '-1.000123456789E+3'
    )
    assert obj(-10000) == '-10E+3'
    assert obj(-10000.1234567890) == (
        '-10.0001234568E+3'
        if sys.hexversion < 0x03000000 else
        '-10.000123456789E+3'
    )
    assert obj(-100000) == '-100E+3'
    assert obj(-100000.1234567890) == (
        '-100.000123457E+3'
        if sys.hexversion < 0x03000000 else
        '-100.000123456789E+3'
    )
    assert obj(-1000000) == '-1E+6'
    assert obj(-1000000.1234567890) == (
        '-1.00000012346E+6'
        if sys.hexversion < 0x03000000 else
        '-1.000000123456789E+6'
    )
    assert obj(-10000000) == '-10E+6'
    assert obj(-10000000.1234567890) == (
        '-10.0000001235E+6'
        if sys.hexversion < 0x03000000 else
        '-10.00000012345679E+6'
    )
    assert obj(-100000000) == '-100E+6'
    assert obj(-100000000.1234567890) == (
        '-100.000000123E+6'
        if sys.hexversion < 0x03000000 else
        '-100.00000012345679E+6'
    )
    assert obj(-1000000000) == '-1E+9'
    assert obj(-1000000000.1234567890) == (
        '-1.00000000012E+9'
        if sys.hexversion < 0x03000000 else
        '-1.0000000001234568E+9'
    )
    assert obj(-10000000000) == '-10E+9'
    assert obj(-10000000000.1234567890) == (
        '-10.0000000001E+9'
        if sys.hexversion < 0x03000000 else
        '-10.000000000123457E+9'
    )
    assert obj(-100000000000) == '-100E+9'
    assert obj(-100000000000.1234567890) == (
        '-100E+9'
        if sys.hexversion < 0x03000000 else
        '-100.00000000012346E+9'
    )
    assert obj(-1000000000000) == '-1E+12'
    assert obj(-1000000000000.1234567890) == (
        '-1E+12'
        if sys.hexversion < 0x03000000 else
        '-1.0000000000001234E+12'
    )
    assert obj(-10000000000000) == '-10E+12'
    assert obj(-10000000000000.1234567890) == (
        '-10E+12'
        if sys.hexversion < 0x03000000 else
        '-10.000000000000123E+12'
    )
    assert obj(-100000000000000) == '-100E+12'
    assert obj(-100000000000000.1234567890) == (
        '-100E+12'
        if sys.hexversion < 0x03000000 else
        '-100.00000000000012E+12'
    )
    assert obj(-1000000000000000) == '-1E+15'
    assert obj(-1000000000000000.1234567890) == (
        '-1E+15'
        if sys.hexversion < 0x03000000 else
        '-1.0000000000000001E+15'
    )
    assert obj(-10000000000000000) == '-10E+15'
    assert obj(-10000000000000000.1234567890) == '-10E+15'
    assert obj(-100000000000000000) == '-100E+15'
    assert obj(-100000000000000000.1234567890) == '-100E+15'
    assert obj(-1000000000000000000) == '-1E+18'
    assert obj(-1000000000000000000.1234567890) == '-1E+18'
    assert obj(-10000000000000000000) == '-10E+18'
    assert obj(-10000000000000000000.1234567890) == '-10E+18'
    assert obj(-100000000000000000000) == '-100E+18'
    assert obj(-100000000000000000000.1234567890) == '-100E+18'
    assert obj(-1000000000000000000000) == '-1E+21'
    assert obj(-1000000000000000000000.1234567890) == '-1E+21'
    assert obj(-10000000000000000000000) == '-10E+21'
    assert obj(-10000000000000000000000.1234567890) == '-10E+21'
    assert obj(-100000000000000000000000) == '-100E+21'
    assert obj(-100000000000000000000000.1234567890) == (
        '-100E+21'
        if sys.hexversion < 0x03000000 else
        '-100.00000000000001E+21'
    )
    assert obj(-1000000000000000000000000) == '-1E+24'
    assert obj(-1000000000000000000000000.1234567890) == '-1E+24'
    assert obj(-10000000000000000000000000) == '-10E+24'
    assert obj(-10000000000000000000000000.1234567890) == '-10E+24'
    assert obj(-100000000000000000000000000) == '-100E+24'
    assert obj(-100000000000000000000000000.1234567890) == '-100E+24'
    # Full precision is retained if number is expressed a string
    assert obj('100000.1234567890') == '100.000123456789E+3'
    assert obj('-100000.1234567890') == '-100.000123456789E+3'


def test_no_exp():
    """ Test no_exp function behavior """
    assert putil.eng.no_exp(0) == '0'
    assert putil.eng.no_exp(0.0) == '0.0'
    assert putil.eng.no_exp(4) == '4'
    assert putil.eng.no_exp(4.0) == '4.0'
    assert putil.eng.no_exp(45) == '45'
    assert putil.eng.no_exp(450) == '450'
    assert putil.eng.no_exp(1234567) == '1234567'
    assert putil.eng.no_exp(4.5) == '4.5'
    assert putil.eng.no_exp(4.1234) == '4.1234'
    assert putil.eng.no_exp(4123.4E4) == '41234000'
    assert putil.eng.no_exp(0.1) == '0.1'
    assert putil.eng.no_exp(1.43E-2) == '0.0143'
    assert putil.eng.no_exp(100000000.0) == '100000000.0'
    assert putil.eng.no_exp(1000000) == '1000000'
    assert putil.eng.no_exp(1e3) == '1000.0'


@pytest.mark.eng
def test_no_ex_exceptions():
    """ Test no_exp function exceptions """
    putil.test.assert_exception(
        putil.eng.no_exp,
        {'number':'a'},
        RuntimeError,
        'Argument `number` is not valid'
    )


@pytest.mark.eng
def test_peng_exceptions():
    """ Test peng function exceptions """
    putil.test.assert_exception(
        putil.eng.peng,
        {'number':['5'], 'frac_length':3, 'rjust':True},
        RuntimeError,
        'Argument `number` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng,
        {'number':5, 'frac_length':3.5, 'rjust':True},
        RuntimeError,
        'Argument `frac_length` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng,
        {'number':5, 'frac_length':-2, 'rjust':True},
        RuntimeError,
        'Argument `frac_length` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng,
        {'number':5, 'frac_length':3, 'rjust':'hello'},
        RuntimeError,
        'Argument `rjust` is not valid'
    )


def test_peng():
    """ Test peng function behavior """
    assert putil.eng.peng(3.0333333333, 1, False) == '3.0'
    assert putil.eng.peng(0, 3, True) == '   0.000 '
    assert putil.eng.peng(0, 3, False) == '0.000'
    assert putil.eng.peng(125.5, 0, False) == '126'
    # Positive
    assert putil.eng.peng(1e-25, 3, True) == '   1.000y'
    assert putil.eng.peng(1e-24, 3, True) == '   1.000y'
    assert putil.eng.peng(1e-23, 3, True) == '  10.000y'
    assert putil.eng.peng(1e-22, 3, True) == ' 100.000y'
    assert putil.eng.peng(1e-21, 3, True) == '   1.000z'
    assert putil.eng.peng(1e-20, 3, True) == '  10.000z'
    assert putil.eng.peng(1e-19, 3, True) == ' 100.000z'
    assert putil.eng.peng(1e-18, 3, True) == '   1.000a'
    assert putil.eng.peng(1e-17, 3, True) == '  10.000a'
    assert putil.eng.peng(1e-16, 3, True) == ' 100.000a'
    assert putil.eng.peng(1e-15, 3, True) == '   1.000f'
    assert putil.eng.peng(1e-14, 3, True) == '  10.000f'
    assert putil.eng.peng(1e-13, 3, True) == ' 100.000f'
    assert putil.eng.peng(1e-12, 3, True) == '   1.000p'
    assert putil.eng.peng(1e-11, 3, True) == '  10.000p'
    assert putil.eng.peng(1e-10, 3, True) == ' 100.000p'
    assert putil.eng.peng(1e-9, 3, True) == '   1.000n'
    assert putil.eng.peng(1e-8, 3, True) == '  10.000n'
    assert putil.eng.peng(1e-7, 3, True) == ' 100.000n'
    assert putil.eng.peng(1e-6, 3, True) == '   1.000u'
    assert putil.eng.peng(1e-5, 3, True) == '  10.000u'
    assert putil.eng.peng(1e-4, 3, True) == ' 100.000u'
    assert putil.eng.peng(1e-3, 3, True) == '   1.000m'
    assert putil.eng.peng(1e-2, 3, True) == '  10.000m'
    assert putil.eng.peng(1e-1, 3, True) == ' 100.000m'
    assert putil.eng.peng(1e-0, 3, True) == '   1.000 '
    assert putil.eng.peng(1e+1, 3, True) == '  10.000 '
    assert putil.eng.peng(1e+2, 3, True) == ' 100.000 '
    assert putil.eng.peng(1e+3, 3, True) == '   1.000k'
    assert putil.eng.peng(1e+4, 3, True) == '  10.000k'
    assert putil.eng.peng(1e+5, 3, True) == ' 100.000k'
    assert putil.eng.peng(1e+6, 3, True) == '   1.000M'
    assert putil.eng.peng(1e+7, 3, True) == '  10.000M'
    assert putil.eng.peng(1e+8, 3, True) == ' 100.000M'
    assert putil.eng.peng(1e+9, 3, True) == '   1.000G'
    assert putil.eng.peng(1e+10, 3, True) == '  10.000G'
    assert putil.eng.peng(1e+11, 3, True) == ' 100.000G'
    assert putil.eng.peng(1e+12, 3, True) == '   1.000T'
    assert putil.eng.peng(1e+13, 3, True) == '  10.000T'
    assert putil.eng.peng(1e+14, 3, True) == ' 100.000T'
    assert putil.eng.peng(1e+15, 3, True) == '   1.000P'
    assert putil.eng.peng(1e+16, 3, True) == '  10.000P'
    assert putil.eng.peng(1e+17, 3, True) == ' 100.000P'
    assert putil.eng.peng(1e+18, 3, True) == '   1.000E'
    assert putil.eng.peng(1e+19, 3, True) == '  10.000E'
    assert putil.eng.peng(1e+20, 3, True) == ' 100.000E'
    assert putil.eng.peng(1e+21, 3, True) == '   1.000Z'
    assert putil.eng.peng(1e+22, 3, True) == '  10.000Z'
    assert putil.eng.peng(1e+23, 3, True) == ' 100.000Z'
    assert putil.eng.peng(1e+24, 3, True) == '   1.000Y'
    assert putil.eng.peng(1e+25, 3, True) == '  10.000Y'
    assert putil.eng.peng(1e+26, 3, True) == ' 100.000Y'
    assert putil.eng.peng(1e+27, 3, True) == ' 999.999Y'
    assert putil.eng.peng(12.45, 1, True) == '  12.5 '
    assert putil.eng.peng(998.999e3, 1, True) == ' 999.0k'
    assert putil.eng.peng(998.999e3, 1, False) == '999.0k'
    assert putil.eng.peng(999.999e3, 1, True) == '   1.0M'
    assert putil.eng.peng(999.999e3, 1) == '   1.0M'
    assert putil.eng.peng(999.999e3, 1, False) == '1.0M'
    assert putil.eng.peng(0.995, 0, False) == '995m'
    assert putil.eng.peng(0.9999, 0, False) == '1'
    assert putil.eng.peng(1.9999, 0, False) == '2'
    assert putil.eng.peng(999.99, 0, False) == '1k'
    assert putil.eng.peng(9.99, 1, False) == '10.0'
    assert putil.eng.peng(5.25e3, 1, True) == '   5.3k'
    assert putil.eng.peng(1.05e3, 0, True) == '   1k'
    # Negative
    assert putil.eng.peng(-1e-25, 3, True) == '  -1.000y'
    assert putil.eng.peng(-1e-24, 3, True) == '  -1.000y'
    assert putil.eng.peng(-1e-23, 3, True) == ' -10.000y'
    assert putil.eng.peng(-1e-22, 3, True) == '-100.000y'
    assert putil.eng.peng(-1e-21, 3, True) == '  -1.000z'
    assert putil.eng.peng(-1e-20, 3, True) == ' -10.000z'
    assert putil.eng.peng(-1e-19, 3, True) == '-100.000z'
    assert putil.eng.peng(-1e-18, 3, True) == '  -1.000a'
    assert putil.eng.peng(-1e-17, 3, True) == ' -10.000a'
    assert putil.eng.peng(-1e-16, 3, True) == '-100.000a'
    assert putil.eng.peng(-1e-15, 3, True) == '  -1.000f'
    assert putil.eng.peng(-1e-14, 3, True) == ' -10.000f'
    assert putil.eng.peng(-1e-13, 3, True) == '-100.000f'
    assert putil.eng.peng(-1e-12, 3, True) == '  -1.000p'
    assert putil.eng.peng(-1e-11, 3, True) == ' -10.000p'
    assert putil.eng.peng(-1e-10, 3, True) == '-100.000p'
    assert putil.eng.peng(-1e-9, 3, True) == '  -1.000n'
    assert putil.eng.peng(-1e-8, 3, True) == ' -10.000n'
    assert putil.eng.peng(-1e-7, 3, True) == '-100.000n'
    assert putil.eng.peng(-1e-6, 3, True) == '  -1.000u'
    assert putil.eng.peng(-1e-5, 3, True) == ' -10.000u'
    assert putil.eng.peng(-1e-4, 3, True) == '-100.000u'
    assert putil.eng.peng(-1e-3, 3, True) == '  -1.000m'
    assert putil.eng.peng(-1e-2, 3, True) == ' -10.000m'
    assert putil.eng.peng(-1e-1, 3, True) == '-100.000m'
    assert putil.eng.peng(-1e-0, 3, True) == '  -1.000 '
    assert putil.eng.peng(-1e+1, 3, True) == ' -10.000 '
    assert putil.eng.peng(-1e+2, 3, True) == '-100.000 '
    assert putil.eng.peng(-1e+3, 3, True) == '  -1.000k'
    assert putil.eng.peng(-1e+4, 3, True) == ' -10.000k'
    assert putil.eng.peng(-1e+5, 3, True) == '-100.000k'
    assert putil.eng.peng(-1e+6, 3, True) == '  -1.000M'
    assert putil.eng.peng(-1e+7, 3, True) == ' -10.000M'
    assert putil.eng.peng(-1e+8, 3, True) == '-100.000M'
    assert putil.eng.peng(-1e+9, 3, True) == '  -1.000G'
    assert putil.eng.peng(-1e+10, 3, True) == ' -10.000G'
    assert putil.eng.peng(-1e+11, 3, True) == '-100.000G'
    assert putil.eng.peng(-1e+12, 3, True) == '  -1.000T'
    assert putil.eng.peng(-1e+13, 3, True) == ' -10.000T'
    assert putil.eng.peng(-1e+14, 3, True) == '-100.000T'
    assert putil.eng.peng(-1e+15, 3, True) == '  -1.000P'
    assert putil.eng.peng(-1e+16, 3, True) == ' -10.000P'
    assert putil.eng.peng(-1e+17, 3, True) == '-100.000P'
    assert putil.eng.peng(-1e+18, 3, True) == '  -1.000E'
    assert putil.eng.peng(-1e+19, 3, True) == ' -10.000E'
    assert putil.eng.peng(-1e+20, 3, True) == '-100.000E'
    assert putil.eng.peng(-1e+21, 3, True) == '  -1.000Z'
    assert putil.eng.peng(-1e+22, 3, True) == ' -10.000Z'
    assert putil.eng.peng(-1e+23, 3, True) == '-100.000Z'
    assert putil.eng.peng(-1e+24, 3, True) == '  -1.000Y'
    assert putil.eng.peng(-1e+25, 3, True) == ' -10.000Y'
    assert putil.eng.peng(-1e+26, 3, True) == '-100.000Y'
    assert putil.eng.peng(-1e+27, 3, True) == '-999.999Y'
    assert putil.eng.peng(-12.45, 1, True) == ' -12.5 '
    assert putil.eng.peng(-998.999e3, 1, True) == '-999.0k'
    assert putil.eng.peng(-998.999e3, 1, False) == '-999.0k'
    assert putil.eng.peng(-999.999e3, 1, True) == '  -1.0M'
    assert putil.eng.peng(-999.999e3, 1) == '  -1.0M'
    assert putil.eng.peng(-999.999e3, 1, False) == '-1.0M'
    assert putil.eng.peng(-0.995, 0, False) == '-995m'
    assert putil.eng.peng(-0.9999, 0, False) == '-1'
    assert putil.eng.peng(-1.9999, 0, False) == '-2'
    assert putil.eng.peng(-999.99, 0, False) == '-1k'
    assert putil.eng.peng(-9.99, 1, False) == '-10.0'
    assert putil.eng.peng(-5.25e3, 1, True) == '  -5.3k'
    assert putil.eng.peng(-1.05e3, 0, True) == '  -1k'


@pytest.mark.eng
def test_peng_float_exceptions():
    """ Test peng_float function exceptions """
    putil.test.assert_exception(
        putil.eng.peng_float,
        {'snum':None},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_float,
        {'snum':5},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_float,
        {'snum':''},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_float,
        {'snum':' 5x'},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_float,
        {'snum':'a5M'},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_float,
        {'snum':'- - a5M'},
        RuntimeError,
        'Argument `snum` is not valid'
    )


def test_peng_float():
    """ Test peng_float function behavior """
    assert putil.eng.peng_float(putil.eng.peng(5234.567, 3, True)) == 5.235e3
    assert putil.eng.peng_float('     5.235k    ') == 5.235e3
    assert putil.eng.peng_float('    -5.235k    ') == -5.235e3


@pytest.mark.eng
def test_peng_frac_exceptions():
    """ Test peng_frac function exceptions """
    putil.test.assert_exception(
        putil.eng.peng_frac,
        {'snum':None},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_frac,
        {'snum':''},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_frac,
        {'snum':' 5x'},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_frac,
        {'snum':'a5M'},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_frac,
        {'snum':'- - a5M'},
        RuntimeError,
        'Argument `snum` is not valid'
    )


def test_peng_frac():
    """ Test peng_frac function behavior """
    assert putil.eng.peng_frac(putil.eng.peng(5234.567, 6, True)) == 234567
    assert putil.eng.peng_frac(putil.eng.peng(5234, 0, True)) == 0


@pytest.mark.eng
def test_peng_int_exceptions():
    """ Test peng_int function exceptions """
    putil.test.assert_exception(
        putil.eng.peng_int,
        {'snum':None},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_int,
        {'snum':''},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_int,
        {'snum':' 5x'},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_int,
        {'snum':'a5M'},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_int,
        {'snum':'- - a5M'},
        RuntimeError,
        'Argument `snum` is not valid'
    )


def test_peng_int():
    """ Test peng_int function behavior """
    assert putil.eng.peng_int(putil.eng.peng(5234.567, 6, True)) == 5


@pytest.mark.eng
def test_peng_mant_exceptions():
    """ Test peng_mant function exceptions """
    putil.test.assert_exception(
        putil.eng.peng_mant,
        {'snum':None},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_mant,
        {'snum':''},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_mant,
        {'snum':' 5x'},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_mant,
        {'snum':'a5M'},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_mant,
        {'snum':'- - a5M'},
        RuntimeError,
        'Argument `snum` is not valid'
    )


def test_peng_mant():
    """ Test peng_mant function behavior """
    assert putil.eng.peng_mant(putil.eng.peng(5234.567, 3, True)) == 5.235


@pytest.mark.eng
def test_peng_power_exceptions():
    """ Test peng_power function exceptions """
    putil.test.assert_exception(
        putil.eng.peng_power,
        {'snum':None},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_power,
        {'snum':''},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_power,
        {'snum':' 5x'},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_power,
        {'snum':'a5M'},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_power,
        {'snum':'- - a5M'},
        RuntimeError,
        'Argument `snum` is not valid'
    )


def test_peng_power():
    """ Test peng_power function behavior """
    tup = putil.eng.peng_power(putil.eng.peng(1234.567, 3, True))
    assert tup == ('k', 1000.0)
    assert isinstance(tup[1], float)


@pytest.mark.eng
def test_peng_suffix_exceptions():
    """ Test peng_suffix function exceptions """
    putil.test.assert_exception(
        putil.eng.peng_suffix,
        {'snum':None},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_suffix,
        {'snum':''},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_suffix,
        {'snum':' 5x'},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_suffix,
        {'snum':'a5M'},
        RuntimeError,
        'Argument `snum` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_suffix,
        {'snum':'- - a5M'},
        RuntimeError,
        'Argument `snum` is not valid'
    )


def test_peng_suffix():
    """ Test peng_suffix function behavior """
    assert putil.eng.peng_suffix(putil.eng.peng(1, 3, True)) == ' '
    assert putil.eng.peng_suffix(putil.eng.peng(-10.5e-6, 3, False)) == 'u'


@pytest.mark.eng
def test_peng_suffix_math_exceptions():
    """ Test peng_suffix_math function exceptions """
    putil.test.assert_exception(
        putil.eng.peng_suffix_math,
        {'suffix':'X', 'offset':-1},
        RuntimeError,
        'Argument `suffix` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_suffix_math,
        {'suffix':'M', 'offset':'a'},
        RuntimeError,
        'Argument `offset` is not valid'
    )
    putil.test.assert_exception(
        putil.eng.peng_suffix_math,
        {'suffix':'M', 'offset':20},
        ValueError,
        'Argument `offset` is not valid'
    )


def test_peng_suffix_math():
    """ Test peng_suffix_math function behavior """
    assert putil.eng.peng_suffix_math(' ', 3) == 'G'
    assert putil.eng.peng_suffix_math('u', -2) == 'p'


def test_to_scientific_string():
    """ Test _to_scientific function behavior """
    obj = putil.eng.to_scientific_string
    # Standard floating point mantissa length appears to be 12 digits
    # Positive
    assert obj('5.35E+3') == '5.35E+3'
    assert obj(0) == '0E+0'
    assert obj(0.1) == '1E-1'
    assert obj(0.01) == '1E-2'
    assert obj(0.001) == '1E-3'
    assert obj(0.00101) == '1.01E-3'
    assert obj(0.123456789012) == '1.23456789012E-1'
    assert obj(1234567.89012) == '1.23456789012E+6'
    assert obj(1) == '1E+0'
    assert obj(20) == '2E+1'
    assert obj(100) == '1E+2'
    assert obj(200) == '2E+2'
    assert obj(333) == '3.33E+2'
    assert obj(4567) == '4.567E+3'
    assert obj(4567.890) == '4.56789E+3'
    assert obj(500, 3) == '5.000E+2'
    assert obj(4567.890, 8) == '4.56789000E+3'
    assert obj(99.999, 1) == '1.0E+2'
    assert obj(4567.890, sign_always=True) == '+4.56789E+3'
    assert obj(500, 3, sign_always=True) == '+5.000E+2'
    assert obj(4567.890, 8, sign_always=True) == '+4.56789000E+3'
    assert obj(99.999, 1, sign_always=True) == '+1.0E+2'
    assert obj(500, 3, 2, sign_always=True) == '+5.000E+02'
    assert obj(4567.890, 8, 3, sign_always=True) == '+4.56789000E+003'
    assert obj(9999999999.999, 1, 1, sign_always=True) == '+1.0E+10'
    # Negative
    assert obj(-0.1) == '-1E-1'
    assert obj(-0.01) == '-1E-2'
    assert obj(-0.001) == '-1E-3'
    assert obj(-0.00101) == '-1.01E-3'
    assert obj(-0.123456789012) == '-1.23456789012E-1'
    assert obj(-1234567.89012) == '-1.23456789012E+6'
    assert obj(-1) == '-1E+0'
    assert obj(-20) == '-2E+1'
    assert obj(-100) == '-1E+2'
    assert obj(-200) == '-2E+2'
    assert obj(-333) == '-3.33E+2'
    assert obj(-4567) == '-4.567E+3'
    assert obj(-4567.890) == '-4.56789E+3'
    assert obj(-500, 3) == '-5.000E+2'
    assert obj(-4567.890, 8) == '-4.56789000E+3'
    assert obj(-99.999, 1) == '-1.0E+2'
    assert obj(-4567.890, sign_always=True) == '-4.56789E+3'
    assert obj(-500, 3, sign_always=True) == '-5.000E+2'
    assert obj(-4567.890, 8, sign_always=True) == '-4.56789000E+3'
    assert obj(-99.999, 1, sign_always=True) == '-1.0E+2'
    assert obj(-500, 3, 2, sign_always=True) == '-5.000E+02'
    assert obj(-4567.890, 8, 3, sign_always=True) == '-4.56789000E+003'
    assert obj(-9999999999.999, 1, 1, sign_always=True) == '-1.0E+10'


def test_pprint_vector():
    """ Test pprint_vector function behavior """
    obj = putil.eng.pprint_vector
    ref = 'None'
    assert obj(None) == ref
    # Float and integer items
    ref = '[ 1, 2, 3, 4, 5, 6, 7, 8 ]'
    assert obj([1, 2, 3, 4, 5, 6, 7, 8]) == ref
    ref = '[ 1, 2, 3, 4, 5, 6, 7, 8 ]'
    assert obj([1, 2, 3, 4, 5, 6, 7, 8], indent=20) == ref
    ref = '[ 1, 2, 3, ..., 6, 7, 8 ]'
    assert obj([1, 2, 3, 4, 5, 6, 7, 8], limit=True) == ref
    ref = '[ 1, 2, 3, ..., 6, 7, 8 ]'
    assert obj([1, 2, 3, 4, 5, 6, 7, 8], limit=True, indent=20) == ref
    ref = (
        '[    1.000m,   20.000u,  300.000M,    4.000p,'
        '    5.250k,   -6.000n,  700.000 ,  800.000m ]'
    )
    assert obj(
        [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
        eng=True) == ref
    ref = (
        '[    1.000m,   20.000u,  300.000M,    4.000p,'
        '    5.250k,   -6.000n,  700.000 ,  800.000m ]'
    )
    assert (
        obj(
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            eng=True,
            indent=20
        )
        ==
        ref
    )
    ref = (
        '[    1.000m,   20.000u,  300.000M,'
        ' ...,'
        '   -6.000n,  700.000 ,  800.000m ]'
    )
    assert (
        obj(
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            limit=True,
            eng=True
        )
        ==
        ref
    )
    ref = (
        '[    1.000m,   20.000u,  300.000M,'
        ' ...,'
        '   -6.000n,  700.000 ,  800.000m ]'
    )
    assert (
        obj(
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            limit=True,
            eng=True,
            indent=20
        )
        ==
        ref
    )
    ref = (
        '[    1.0m,   20.0u,  300.0M,    4.0p,'
        '    5.3k,   -6.0n,  700.0 ,  800.0m ]'
    )
    assert (
        obj(
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            eng=True,
            frac_length=1
        )
        ==
        ref
    )
    ref = (
        '[    1.0m,   20.0u,  300.0M,    4.0p,'
        '    5.3k,   -6.0n,  700.0 ,  800.0m ]'
    )
    assert (
        obj(
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            eng=True,
            frac_length=1,
            indent=20
        )
        ==
        ref
    )
    ref = '[    1.0m,   20.0u,  300.0M, ...,   -6.0n,  700.0 ,  800.0m ]'
    assert (
        obj(
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            limit=True,
            eng=True,
            frac_length=1
        )
        ==
        ref
    )
    ref = '[    1.0m,   20.0u,  300.0M, ...,   -6.0n,  700.0 ,  800.0m ]'
    assert (
        obj(
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            limit=True,
            indent=20,
            eng=True,
            frac_length=1
        )
        ==
        ref
    )
    ref = (
        #12345678
        '[ 1, 2,\n'
        '  3, 4,\n'
        '  5, 6,\n'
        '  7, 8 ]'
    )
    assert obj([1, 2, 3, 4, 5, 6, 7, 8], width=8) == ref
    ref = '[ 1, 2, 3,\n  4, 5, 6,\n  7, 8 ]'
    assert obj([1, 2, 3, 4, 5, 6, 7, 8], width=10) == ref
    ref = (
        '[    1m,   20u,\n'
        '   300M,    4p,\n'
        '     5k,   -6n,\n'
        '   700 ,    8 ,\n'
        '     9  ]'
    )
    assert (
        obj(
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 8, 9],
            width=20,
            eng=True,
            frac_length=0
        )
        ==
        ref
    )
    ref = (
        '[    1.0m,   20.0u,  300.0M,\n'
        '     4.0p,    5.3k,   -6.0n,\n'
        '   700.0 ,  800.0m ]'
    )
    assert (
        obj(
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            width=30,
            eng=True,
            frac_length=1
        )
        ==
        ref
    )
    ref = (
        '[    1m,\n'
        '    20u,\n'
        '   300M,\n'
        '   ...\n'
        '   700 ,\n'
        '     8 ,\n'
        '     9  ]'
    )
    assert (
        obj(
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 8, 9],
            width=20,
            eng=True,
            frac_length=0,
            limit=True
        )
        ==
        ref
    )
    ref = (
        '[    1.0m,   20.0u,  300.0M,\n'
        '             ...\n'
        '   700.0 ,    8.0 ,    9.0  ]'
    )
    assert (
        obj(
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 8, 9],
            width=30,
            eng=True,
            frac_length=1,
            limit=True
        )
        ==
        ref
    )
    header = 'Vector: '
    ref = (
        'Vector: [    1.0m,   20.0u,  300.0M,\n'
        '                     ...\n'
        '           700.0 ,    8.0 ,    9.0  ]'
    )
    assert (
        header+putil.eng.pprint_vector(
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 8, 9],
            width=30,
            eng=True,
            frac_length=1,
            limit=True,
            indent=len(header)
        )
        ==
        ref
    )
    ref = (
        'Vector: [    1.0m,   20.0u,  300.0M,\n'
        '             4.0p,    5.3k,   -6.0n,\n'
        '           700.0 ,  800.0m ]'
    )
    assert (
        header+putil.eng.pprint_vector(
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            width=30,
            eng=True,
            frac_length=1,
            indent=len(header)
        )
        ==
        ref
    )
    ref = (
        'Independent variable: [ 1.23456789, 2.45678901, 3.45678901,\n'
        '                                        ...\n'
        '                        5.67890123, 6.78901234, 7.89012345 ]'
    )
    assert (
        'Independent variable: '+putil.eng.pprint_vector(
            [
                1.23456789,
                2.45678901,
                3.45678901,
                4.56789012,
                5.67890123,
                6.78901234,
                7.89012345
            ],
            limit=True,
            width=80-22,
            indent=22
        )
        ==
        ref
    )
    ref = (
        'Independent var: [ 1.23456789, 2.45678901, 3.45678901, 4.56789012,\n'
        '                   5.67890123, 6.78901234, 7.89012345 ]'
    )
    assert (
        'Independent var: '+putil.eng.pprint_vector(
            [
                1.23456789,
                2.45678901,
                3.45678901,
                4.56789012,
                5.67890123,
                6.78901234,
                7.89012345
            ],
            width=49,
            indent=17
        )
        ==
        ref
    )
    # Complex items
    cf = complex
    ref = '[ -1+2j, 3+4j, 5+6j, 7+8j, 9-10j, 11+12j, -13+14j, 15678-16j ]'
    vector = [
        cf(-1, 2),
        cf(3, 4),
        cf(5, 6),
        cf(7, 8),
        cf(9, -10),
        cf(11, 12),
        cf(-13, 14),
        cf(15678, -16)
    ]
    assert obj(vector) == ref
    assert obj(vector, indent=20) == ref
    ref = '[ -1+2j, 3+4j, 5+6j, ..., 11+12j, -13+14j, 15678-16j ]'
    assert obj(vector, limit=True) == ref
    ref = '[ -1+2j, 3+4j, 5+6j, ..., 11+12j, -13+14j, 15678-16j ]'
    assert obj(vector, limit=True, indent=20) == ref
    ref = (
        '[   -1.000 +   2.000 j,    3.000 +   4.000 j,    5.000 +   6.000 j,'
        '    7.000 +   8.000 j,    9.000 -  10.000 j,   11.000 +  12.000 j,'
        '  -13.000 +  14.000 j,   15.678k-  16.000 j ]'
    )
    assert obj(vector, eng=True) == ref
    assert obj(vector, eng=True, indent=20) == ref
    ref = (
        '[   -1.000 +   2.000 j,    3.000 +   4.000 j,    5.000 +   6.000 j,'
        ' ...,   11.000 +  12.000 j,  -13.000 +  14.000 j,'
        '   15.678k-  16.000 j ]'
    )
    assert obj(vector, limit=True, eng=True) == ref
    assert obj(vector, limit=True, eng=True, indent=20) == ref
    ref = (
        '[   -1.0 +   2.0 j,    3.0 +   4.0 j,    5.0 +   6.0 j,'
        '    7.0 +   8.0 j,    9.0 -  10.0 j,   11.0 +  12.0 j,'
        '  -13.0 +  14.0 j,   15.7k-  16.0 j ]'
    )
    assert obj(vector, eng=True, frac_length=1) == ref
    assert obj(vector, eng=True, frac_length=1, indent=20) == ref
    ref = (
        '[   -1.0 +   2.0 j,    3.0 +   4.0 j,    5.0 +   6.0 j,'
        ' ...,   11.0 +  12.0 j,  -13.0 +  14.0 j,   15.7k-  16.0 j ]'
    )
    assert obj(vector, limit=True, eng=True, frac_length=1) == ref
    assert obj(vector, limit=True, eng=True, frac_length=1, indent=20) == ref
    ref = (
        '[ -1+2j, 3+4j, 5+6j,\n'
        '  7+8j, 9-10j, 11+12j,\n'
        '  -13+14j, 15678-16j ]'
    )
    assert obj(vector, width=22) == ref
    ref = (
        '[ -1+2j, 3+4j, 5+6j,\n'
        '  7+8j, 9-10j,\n'
        '  11+12j, -13+14j,\n'
        '  15678-16j ]'
    )
    assert obj(vector, width=20) == ref
    ref = (
        '[   -1 +   2 j,    3 +   4 j,\n'
        '     5 +   6 j,    7 +   8 j,\n'
        '     9 -  10 j,   11 +  12 j,\n'
        '   -13 +  14 j,   16k-  16 j ]'
    )
    assert obj(vector, width=29, eng=True, frac_length=0) == ref
    ref = (
        '[   -1.0 +   2.0 j,    3.0 +   4.0 j,\n'
        '     5.0 +   6.0 j,    7.0 +   8.0 j,\n'
        '     9.0 -  10.0 j,   11.0 +  12.0 j,\n'
        '   -13.0 +  14.0 j,   15.7k-  16.0 j ]'
    )
    assert obj(vector, width=37, eng=True, frac_length=1) == ref
    ref = (
        '[   -1 +   2 j,\n'
        '     3 +   4 j,\n'
        '     5 +   6 j,\n'
        '     7 +   8 j,\n'
        '     9 -  10 j,\n'
        '    11 +  12 j,\n'
        '   -13 +  14 j,\n'
        '    16k-  16 j ]'
    )
    assert obj(vector, width=16, eng=True, frac_length=0) == ref
    ref = (
        '[   -1 +   2 j,\n'
        '     3 +   4 j,\n'
        '     5 +   6 j,\n'
        '       ...\n'
        '    11 +  12 j,\n'
        '   -13 +  14 j,\n'
        '    16k-  16 j ]'
    )
    assert obj(vector, width=16, eng=True, frac_length=0, limit=True) == ref
    ref = (
        '[   -1.0 +   2.0 j,    3.0 +   4.0 j,    5.0 +   6.0 j,\n'
        '                           ...\n'
        '    11.0 +  12.0 j,  -13.0 +  14.0 j,   15.7k-  16.0 j ]'
    )
    assert obj(vector, width=56, eng=True, frac_length=1, limit=True) == ref
    ref = (
        'Vector: [   -1.0 +   2.0 j,    3.0 +   4.0 j,    5.0 +   6.0 j,\n'
        '                                   ...\n'
        '            11.0 +  12.0 j,  -13.0 +  14.0 j,   15.7k-  16.0 j ]'
    )
    header = 'Vector: '
    assert (
        header+obj(
            vector,
            width=64,
            eng=True,
            frac_length=1,
            limit=True,
            indent=len(header)
        )
        ==
        ref
    )
    ref = (
        'Vector: [ -1+2j, 3+4j, 5+6j,\n'
        '          7+8j, 9-10j,\n'
        '          11+12j, -13+14j,\n'
        '          15678-16j ]'
    )
    assert (
        header+obj(
            vector,
            width=20,
            indent=len(header)
        )
        ==
        ref
    )
    ref = (
        'Vector: [ -1+2j, 3+4j, 5+6j,\n'
        '                 ...\n'
        '          11+12j, -13+14j, 15678-16j ]'
    )
    assert (
        header+obj(
            vector,
            width=30,
            indent=len(header),
            limit=True
        )
        ==
        ref
    )
    ref = (
        'Vector: [ -1+2j,\n'
        '          3+4j,\n'
        '          5+6j,\n'
        '           ...\n'
        '          11+12j,\n'
        '          -13+14j,\n'
        '          15678-16j ]'
    )
    assert (
        header+obj(
            vector,
            width=20,
            indent=len(header),
            limit=True
        )
        ==
        ref
    )
    vector = numpy.array(
        [
            cf(-0.10081675027325637, -0.06910517142735251),
            cf(0.018754229185649937, 0.017142783560861786),
            cf(0, 18)
        ]
    )
    ref = (
        '[ '
        '-0.100816750273-0.0691051714274j, '
        '0.0187542291856+0.0171427835609j, '
        '18j '
        ']'
    )
    assert obj(vector) == ref
    ref = (
        'Dependent variable: [ -0.100816750273-0.0691051714274j,\n'
        '                      0.0187542291856+0.0171427835609j, 18j ]'
    )
    assert (
        'Dependent variable: '+obj(vector, width=60, limit=True, indent=20)
        ==
        ref
    )
    vector = numpy.array(
        [
            cf(-0.10081675027325637, -0.06910517142735251),
            cf(0.018754229185649937, 0.017142783560861786),
            cf(0, 18),
            cf(0.118754229185649937, 0.117142783560861786),
            cf(0.218754229185649937, 0.217142783560861786),
            cf(0, 28),
            cf(10, 2),
        ]
    )
    ref = (
        '[ -0.100816750273-0.0691051714274j,\n'
        '  0.0187542291856+0.0171427835609j, 18j,\n'
        '  0.118754229186+0.117142783561j,\n'
        '  0.218754229186+0.217142783561j, 28j, 10+2j ]'
    )
    assert obj(vector, width=60) == ref
    ref = (
        '[ -0.100816750273-0.0691051714274j,\n'
        '  0.0187542291856+0.0171427835609j,\n'
        '  18j,\n'
        '                 ...\n'
        '  0.218754229186+0.217142783561j,\n'
        '  28j,\n'
        '  10+2j ]'
    )
    assert obj(vector, width=60, limit=True) == ref


@pytest.mark.eng
def test_pprint_vector_exceptions():
    """ Test pprint_vector function exceptions """
    putil.test.assert_exception(
        putil.eng.pprint_vector,
        {
            'vector':[1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 8, 9],
            'width':5, 'eng':True, 'frac_length':1, 'limit':True
        },
        ValueError,
        'Argument `width` is too small'
    )
    cf = complex
    vector = [
        cf(-1, 2),
        cf(3, 4),
        cf(5, 6),
        cf(7, 8),
        cf(9, -10),
        cf(11, 12),
        cf(-13, 14),
        cf(15678, -16)
    ]
    putil.test.assert_exception(
        putil.eng.pprint_vector,
        {'vector':vector, 'width':8, 'limit':True},
        ValueError,
        'Argument `width` is too small'
    )


def test_round_mantissa():
    """ Test round_mantissa function behavior """
    obj = putil.eng.round_mantissa
    assert obj(None) is None
    assert obj(1.3333, 2) == 1.33
    assert obj(1.5555E-12, 2) == 1.56E-12
    assert obj(3, 2) == 3
    ref = numpy.array([1.33, 2.67])
    assert (obj(numpy.array([1.3333, 2.666666]), 2) == ref).all()
    ref = numpy.array([1.33E-12, 2.67E-12])
    assert (obj(numpy.array([1.3333E-12, 2.666666E-12]), 2) == ref).all()
    ref = numpy.array([1, 3])
    assert (obj(numpy.array([1, 3]), 2) == ref).all()
