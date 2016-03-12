# test_eng.py
# Copyright (c) 2013-2016 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0103,C0111,C0302,E0611,R0913,R0915,W0108,W0212

# Standard library imports
import functools
import sys
import pytest
from numpy import array, ndarray
# Putil imports
import putil.test
import putil.eng


###
# Global variables
###
AE = functools.partial(putil.test.assert_exception, extype=RuntimeError)
DFLT = 'def'
PY2 = bool(sys.hexversion < 0x03000000)

###
# Helper functions
###
isdflt = lambda obj: bool(obj == DFLT)
h = lambda num: '100.'+('0'*num)
o = lambda num: '1.'+('0'*num)
pv = lambda py2arg, py3arg: py2arg if PY2 else py3arg
sarg = lambda msg: 'Argument `{0}` is not valid'.format(msg)
t = lambda num: '10.'+('0'*num)


###
# Test functions
###
@pytest.mark.parametrize(
    'text, sep, num, lstrip, rstrip, ref', [
    ('a, b, c, d', ',', 1, DFLT, DFLT, ['a', ' b', ' c', ' d']),
    ('a , b , c , d ', ',', 1, DFLT, DFLT, ['a ', ' b ', ' c ', ' d ']),
    ('a , b , c , d ', ',', 1, True, DFLT, ['a ', 'b ', 'c ', 'd ']),
    ('a , b , c , d ', ',', 1, DFLT, True, ['a', ' b', ' c', ' d']),
    ('a , b , c , d ', ',', 1, True, True, ['a', 'b', 'c', 'd']),
    ('a, b, c, d', ',', 2, DFLT, DFLT, ['a, b', ' c, d']),
    ('a, b, c, d', ',', 3, DFLT, DFLT, ['a, b, c', ' d']),
    ('a, b, c, d', ',', 4, DFLT, DFLT, ['a, b, c, d']),
    ('a, b, c, d', ',', 5, DFLT, DFLT, ['a, b, c, d']),
    ]
)
def test_split_every(text, sep, num, lstrip, rstrip, ref):
    """ Test _split_every function behavior """
    # DFLT in lstrip or rstrip means default argument values should be used
    obj = putil.eng._split_every
    obj = obj if isdflt(lstrip) else functools.partial(obj, lstrip=lstrip)
    obj = obj if isdflt(rstrip) else functools.partial(obj, rstrip=rstrip)
    assert obj(text, sep, num) == ref


@pytest.mark.parametrize(
    'num, ref', [
    (0.000000000000000000000001001234567890, '1.00123456789E-24'),
    (0.000000000000000000000001, '1E-24'),
    (0.00000000000000000000001001234567890, '10.0123456789E-24'),
    (0.00000000000000000000001, '10E-24'),
    (0.0000000000000000000001001234567890, '100.123456789E-24'),
    (0.0000000000000000000001, '100E-24'),
    (0.000000000000000000001001234567890, '1.00123456789E-21'),
    (0.000000000000000000001, '1E-21'),
    (0.00000000000000000001001234567890, '10.0123456789E-21'),
    (0.00000000000000000001, '10E-21'),
    (0.0000000000000000001001234567890, '100.123456789E-21'),
    (0.0000000000000000001, '100E-21'),
    (0.000000000000000001001234567890, '1.00123456789E-18'),
    (0.000000000000000001, '1E-18'),
    (0.00000000000000001001234567890, '10.0123456789E-18'),
    (0.00000000000000001, '10E-18'),
    (0.0000000000000001001234567890, '100.123456789E-18'),
    (0.0000000000000001, '100E-18'),
    (0.000000000000001001234567890, '1.00123456789E-15'),
    (0.000000000000001, '1E-15'),
    (0.00000000000001001234567890, '10.0123456789E-15'),
    (0.00000000000001, '10E-15'),
    (0.0000000000001001234567890, '100.123456789E-15'),
    (0.0000000000001, '100E-15'),
    (0.000000000001001234567890, '1.00123456789E-12'),
    (0.000000000001, '1E-12'),
    (0.00000000001001234567890, '10.0123456789E-12'),
    (0.00000000001, '10E-12'),
    (0.0000000001001234567890, '100.123456789E-12'),
    (0.0000000001, '100E-12'),
    (0.000000001001234567890, '1.00123456789E-9'),
    (0.000000001, '1E-9'),
    (0.00000001001234567890, '10.0123456789E-9'),
    (0.00000001, '10E-9'),
    (0.0000001001234567890, '100.123456789E-9'),
    (0.0000001, '100E-9'),
    (0.000001001234567890, '1.00123456789E-6'),
    (0.000001, '1E-6'),
    (0.00001001234567890, '10.0123456789E-6'),
    (0.00001, '10E-6'),
    (0.0001001234567890, '100.123456789E-6'),
    (0.0001, '100E-6'),
    (0.001001234567890, '1.00123456789E-3'),
    (0.001, '1E-3'),
    (0.01001234567890, '10.0123456789E-3'),
    (0.01, '10E-3'),
    (0.1001234567890, '100.123456789E-3'),
    (0.1, '100E-3'),
    (0, '0E+0'),
    (1, '1E+0'),
    (1.1234567890, '1.123456789E+0'),
    (10, '10E+0'),
    (10.1234567890, '10.123456789E+0'),
    (100, '100E+0'),
    (100.1234567890, '100.123456789E+0'),
    (1000, '1E+3'),
    (1000.1234567890, pv('1.00012345679E+3', '1.000123456789E+3')),
    (10000, '10E+3'),
    (10000.1234567890, pv('10.0001234568E+3', '10.000123456789E+3')),
    (100000, '100E+3'),
    (100000.1234567890, pv('100.000123457E+3', '100.000123456789E+3')),
    (1000000, '1E+6'),
    (1000000.1234567890, pv('1.00000012346E+6', '1.000000123456789E+6')),
    (10000000, '10E+6'),
    (10000000.1234567890, pv('10.0000001235E+6', '10.00000012345679E+6')),
    (100000000, '100E+6'),
    (100000000.1234567890, pv('100.000000123E+6', '100.00000012345679E+6')),
    (1000000000, '1E+9'),
    (1000000000.1234567890, pv('1.00000000012E+9', '1.0000000001234568E+9')),
    (10000000000, '10E+9'),
    (10000000000.1234567890, pv(t(9)+'1E+9', '10.000000000123457E+9')),
    (100000000000, '100E+9'),
    (100000000000.1234567890, pv('100E+9', '100.00000000012346E+9')),
    (1000000000000, '1E+12'),
    (1000000000000.1234567890, pv('1E+12', '1.0000000000001234E+12')),
    (10000000000000, '10E+12'),
    (10000000000000.1234567890, pv('10E+12', '10.000000000000123E+12')),
    (100000000000000, '100E+12'),
    (100000000000000.1234567890, pv('100E+12', '100.00000000000012E+12')),
    (1000000000000000, '1E+15'),
    (1000000000000000.1234567890, pv('1E+15', '1.0000000000000001E+15')),
    (10000000000000000, '10E+15'),
    (10000000000000000.1234567890, '10E+15'),
    (100000000000000000, '100E+15'),
    (100000000000000000.1234567890, '100E+15'),
    (1000000000000000000, '1E+18'),
    (1000000000000000000.1234567890, '1E+18'),
    (10000000000000000000, '10E+18'),
    (10000000000000000000.1234567890, '10E+18'),
    (100000000000000000000, '100E+18'),
    (100000000000000000000.1234567890, '100E+18'),
    (1000000000000000000000, '1E+21'),
    (1000000000000000000000.1234567890, '1E+21'),
    (10000000000000000000000, '10E+21'),
    (10000000000000000000000.1234567890, '10E+21'),
    (100000000000000000000000, '100E+21'),
    (100000000000000000000000.1234567890, pv('100E+21', h(13)+'1E+21')),
    (1000000000000000000000000, '1E+24'),
    (1000000000000000000000000.1234567890, '1E+24'),
    (10000000000000000000000000, '10E+24'),
    (10000000000000000000000000.1234567890, '10E+24'),
    (100000000000000000000000000, '100E+24'),
    (100000000000000000000000000.1234567890, '100E+24'),
    (-0.000000000000000000000001001234567890, '-1.00123456789E-24'),
    (-0.000000000000000000000001, '-1E-24'),
    (-0.00000000000000000000001001234567890, '-10.0123456789E-24'),
    (-0.00000000000000000000001, '-10E-24'),
    (-0.0000000000000000000001001234567890, '-100.123456789E-24'),
    (-0.0000000000000000000001, '-100E-24'),
    (-0.000000000000000000001001234567890, '-1.00123456789E-21'),
    (-0.000000000000000000001, '-1E-21'),
    (-0.00000000000000000001001234567890, '-10.0123456789E-21'),
    (-0.00000000000000000001, '-10E-21'),
    (-0.0000000000000000001001234567890, '-100.123456789E-21'),
    (-0.0000000000000000001, '-100E-21'),
    (-0.000000000000000001001234567890, '-1.00123456789E-18'),
    (-0.000000000000000001, '-1E-18'),
    (-0.00000000000000001001234567890, '-10.0123456789E-18'),
    (-0.00000000000000001, '-10E-18'),
    (-0.0000000000000001001234567890, '-100.123456789E-18'),
    (-0.0000000000000001, '-100E-18'),
    (-0.000000000000001001234567890, '-1.00123456789E-15'),
    (-0.000000000000001, '-1E-15'),
    (-0.00000000000001001234567890, '-10.0123456789E-15'),
    (-0.00000000000001, '-10E-15'),
    (-0.0000000000001001234567890, '-100.123456789E-15'),
    (-0.0000000000001, '-100E-15'),
    (-0.000000000001001234567890, '-1.00123456789E-12'),
    (-0.000000000001, '-1E-12'),
    (-0.00000000001001234567890, '-10.0123456789E-12'),
    (-0.00000000001, '-10E-12'),
    (-0.0000000001001234567890, '-100.123456789E-12'),
    (-0.0000000001, '-100E-12'),
    (-0.000000001001234567890, '-1.00123456789E-9'),
    (-0.000000001, '-1E-9'),
    (-0.00000001001234567890, '-10.0123456789E-9'),
    (-0.00000001, '-10E-9'),
    (-0.0000001001234567890, '-100.123456789E-9'),
    (-0.0000001, '-100E-9'),
    (-0.000001001234567890, '-1.00123456789E-6'),
    (-0.000001, '-1E-6'),
    (-0.00001001234567890, '-10.0123456789E-6'),
    (-0.00001, '-10E-6'),
    (-0.0001001234567890, '-100.123456789E-6'),
    (-0.0001, '-100E-6'),
    (-0.001001234567890, '-1.00123456789E-3'),
    (-0.001, '-1E-3'),
    (-0.01001234567890, '-10.0123456789E-3'),
    (-0.01, '-10E-3'),
    (-0.1001234567890, '-100.123456789E-3'),
    (-0.1, '-100E-3'),
    (-1, '-1E+0'),
    (-1.1234567890, '-1.123456789E+0'),
    (-10, '-10E+0'),
    (-10.1234567890, '-10.123456789E+0'),
    (-100, '-100E+0'),
    (-100.1234567890, '-100.123456789E+0'),
    (-1000, '-1E+3'),
    (-1000.1234567890, pv('-1.00012345679E+3', '-1.000123456789E+3')),
    (-10000, '-10E+3'),
    (-10000.1234567890, pv('-10.0001234568E+3', '-10.000123456789E+3')),
    (-100000, '-100E+3'),
    (-100000.1234567890, pv('-100.000123457E+3', '-100.000123456789E+3')),
    (-1000000, '-1E+6'),
    (-1000000.1234567890, pv('-1.00000012346E+6', '-1.000000123456789E+6')),
    (-10000000, '-10E+6'),
    (-10000000.1234567890, pv('-10.0000001235E+6', '-10.00000012345679E+6')),
    (-100000000, '-100E+6'),
    (-100000000.1234567890, pv('-'+h(6)+'123E+6', '-100.00000012345679E+6')),
    (-1000000000, '-1E+9'),
    (-1000000000.1234567890, pv('-'+o(9)+'12E+9', '-1.0000000001234568E+9')),
    (-10000000000, '-10E+9'),
    (-10000000000.1234567890, pv('-'+t(9)+'1E+9', '-'+t(9)+'123457E+9')),
    (-100000000000, '-100E+9'),
    (-100000000000.1234567890, pv('-100E+9', '-100.00000000012346E+9')),
    (-1000000000000, '-1E+12'),
    (-1000000000000.1234567890, pv('-1E+12', '-1.0000000000001234E+12')),
    (-10000000000000, '-10E+12'),
    (-10000000000000.1234567890, pv('-10E+12', '-10.000000000000123E+12')),
    (-100000000000000, '-100E+12'),
    (-100000000000000.1234567890, pv('-100E+12', '-100.00000000000012E+12')),
    (-1000000000000000, '-1E+15'),
    (-1000000000000000.1234567890, pv('-1E+15', '-1.0000000000000001E+15')),
    (-10000000000000000, '-10E+15'),
    (-10000000000000000.1234567890, '-10E+15'),
    (-100000000000000000, '-100E+15'),
    (-100000000000000000.1234567890, '-100E+15'),
    (-1000000000000000000, '-1E+18'),
    (-1000000000000000000.1234567890, '-1E+18'),
    (-10000000000000000000, '-10E+18'),
    (-10000000000000000000.1234567890, '-10E+18'),
    (-100000000000000000000, '-100E+18'),
    (-100000000000000000000.1234567890, '-100E+18'),
    (-1000000000000000000000, '-1E+21'),
    (-1000000000000000000000.1234567890, '-1E+21'),
    (-10000000000000000000000, '-10E+21'),
    (-10000000000000000000000.1234567890, '-10E+21'),
    (-100000000000000000000000, '-100E+21'),
    (-100000000000000000000000.1234567890, pv('-100E+21', '-'+h(13)+'1E+21')),
    (-1000000000000000000000000, '-1E+24'),
    (-1000000000000000000000000.1234567890, '-1E+24'),
    (-10000000000000000000000000, '-10E+24'),
    (-10000000000000000000000000.1234567890, '-10E+24'),
    (-100000000000000000000000000, '-100E+24'),
    (-100000000000000000000000000.1234567890, '-100E+24'),
    ('100000.1234567890', '100.000123456789E+3'),
    ('-100000.1234567890', '-100.000123456789E+3'),
    ]
)
def test_to_sci_string(num, ref):
    """ Test _to_eng_string function behavior """
    assert putil.eng._to_sci_string(num) == ref


@pytest.mark.parametrize(
    'num, ref', [
    (0, '0'),
    (0.0, '0.0'),
    (4, '4'),
    (4.0, '4.0'),
    (45, '45'),
    (450, '450'),
    (1234567, '1234567'),
    (4.5, '4.5'),
    (4.1234, '4.1234'),
    (4123.4E4, '41234000'),
    (0.1, '0.1'),
    (1.43E-2, '0.0143'),
    (100000000.0, '100000000.0'),
    (1000000, '1000000'),
    (1e3, '1000.0'),
    ]
)
def test_no_exp(num, ref):
    """ Test no_exp function behavior """
    assert putil.eng.no_exp(num) == ref


@pytest.mark.eng
def test_no_ex_exceptions():
    """ Test no_exp function exceptions """
    AE(putil.eng.no_exp, {'number':'a'}, exmsg=sarg('number'))


@pytest.mark.eng
@pytest.mark.parametrize(
    'args, name', [
        (dict(number=['5'], frac_length=3, rjust=True), 'number'),
        (dict(number=5, frac_length=3.5, rjust=True), 'frac_length'),
        (dict(number=5, frac_length=-2, rjust=True), 'frac_length'),
        (dict(number=5, frac_length=3, rjust='a'), 'rjust')
    ]
)
def test_peng_exceptions(args, name):
    """ Test peng function exceptions """
    AE(putil.eng.peng, args, exmsg=sarg(name))


@pytest.mark.parametrize(
    'num, mant, rjust, ref', [
        (3.0333333333, 1, False, '3.0'),
        (0, 3, True, '   0.000 '),
        (0, 3, False, '0.000'),
        (125.5, 0, False, '126'),
        (1e-25, 3, True, '   1.000y'),
        (1e-24, 3, True, '   1.000y'),
        (1e-23, 3, True, '  10.000y'),
        (1e-22, 3, True, ' 100.000y'),
        (1e-21, 3, True, '   1.000z'),
        (1e-20, 3, True, '  10.000z'),
        (1e-19, 3, True, ' 100.000z'),
        (1e-18, 3, True, '   1.000a'),
        (1e-17, 3, True, '  10.000a'),
        (1e-16, 3, True, ' 100.000a'),
        (1e-15, 3, True, '   1.000f'),
        (1e-14, 3, True, '  10.000f'),
        (1e-13, 3, True, ' 100.000f'),
        (1e-12, 3, True, '   1.000p'),
        (1e-11, 3, True, '  10.000p'),
        (1e-10, 3, True, ' 100.000p'),
        (1e-9, 3, True, '   1.000n'),
        (1e-8, 3, True, '  10.000n'),
        (1e-7, 3, True, ' 100.000n'),
        (1e-6, 3, True, '   1.000u'),
        (1e-5, 3, True, '  10.000u'),
        (1e-4, 3, True, ' 100.000u'),
        (1e-3, 3, True, '   1.000m'),
        (1e-2, 3, True, '  10.000m'),
        (1e-1, 3, True, ' 100.000m'),
        (1e-0, 3, True, '   1.000 '),
        (1e+1, 3, True, '  10.000 '),
        (1e+2, 3, True, ' 100.000 '),
        (1e+3, 3, True, '   1.000k'),
        (1e+4, 3, True, '  10.000k'),
        (1e+5, 3, True, ' 100.000k'),
        (1e+6, 3, True, '   1.000M'),
        (1e+7, 3, True, '  10.000M'),
        (1e+8, 3, True, ' 100.000M'),
        (1e+9, 3, True, '   1.000G'),
        (1e+10, 3, True, '  10.000G'),
        (1e+11, 3, True, ' 100.000G'),
        (1e+12, 3, True, '   1.000T'),
        (1e+13, 3, True, '  10.000T'),
        (1e+14, 3, True, ' 100.000T'),
        (1e+15, 3, True, '   1.000P'),
        (1e+16, 3, True, '  10.000P'),
        (1e+17, 3, True, ' 100.000P'),
        (1e+18, 3, True, '   1.000E'),
        (1e+19, 3, True, '  10.000E'),
        (1e+20, 3, True, ' 100.000E'),
        (1e+21, 3, True, '   1.000Z'),
        (1e+22, 3, True, '  10.000Z'),
        (1e+23, 3, True, ' 100.000Z'),
        (1e+24, 3, True, '   1.000Y'),
        (1e+25, 3, True, '  10.000Y'),
        (1e+26, 3, True, ' 100.000Y'),
        (1e+27, 3, True, ' 999.999Y'),
        (12.45, 1, True, '  12.5 '),
        (998.999e3, 1, True, ' 999.0k'),
        (998.999e3, 1, False, '999.0k'),
        (999.999e3, 1, True, '   1.0M'),
        (999.999e3, 1, DFLT, '   1.0M'),
        (999.999e3, 1, False, '1.0M'),
        (0.995, 0, False, '995m'),
        (0.9999, 0, False, '1'),
        (1.9999, 0, False, '2'),
        (999.99, 0, False, '1k'),
        (9.99, 1, False, '10.0'),
        (5.25e3, 1, True, '   5.3k'),
        (1.05e3, 0, True, '   1k'),
        (-1e-25, 3, True, '  -1.000y'),
        (-1e-24, 3, True, '  -1.000y'),
        (-1e-23, 3, True, ' -10.000y'),
        (-1e-22, 3, True, '-100.000y'),
        (-1e-21, 3, True, '  -1.000z'),
        (-1e-20, 3, True, ' -10.000z'),
        (-1e-19, 3, True, '-100.000z'),
        (-1e-18, 3, True, '  -1.000a'),
        (-1e-17, 3, True, ' -10.000a'),
        (-1e-16, 3, True, '-100.000a'),
        (-1e-15, 3, True, '  -1.000f'),
        (-1e-14, 3, True, ' -10.000f'),
        (-1e-13, 3, True, '-100.000f'),
        (-1e-12, 3, True, '  -1.000p'),
        (-1e-11, 3, True, ' -10.000p'),
        (-1e-10, 3, True, '-100.000p'),
        (-1e-9, 3, True, '  -1.000n'),
        (-1e-8, 3, True, ' -10.000n'),
        (-1e-7, 3, True, '-100.000n'),
        (-1e-6, 3, True, '  -1.000u'),
        (-1e-5, 3, True, ' -10.000u'),
        (-1e-4, 3, True, '-100.000u'),
        (-1e-3, 3, True, '  -1.000m'),
        (-1e-2, 3, True, ' -10.000m'),
        (-1e-1, 3, True, '-100.000m'),
        (-1e-0, 3, True, '  -1.000 '),
        (-1e+1, 3, True, ' -10.000 '),
        (-1e+2, 3, True, '-100.000 '),
        (-1e+3, 3, True, '  -1.000k'),
        (-1e+4, 3, True, ' -10.000k'),
        (-1e+5, 3, True, '-100.000k'),
        (-1e+6, 3, True, '  -1.000M'),
        (-1e+7, 3, True, ' -10.000M'),
        (-1e+8, 3, True, '-100.000M'),
        (-1e+9, 3, True, '  -1.000G'),
        (-1e+10, 3, True, ' -10.000G'),
        (-1e+11, 3, True, '-100.000G'),
        (-1e+12, 3, True, '  -1.000T'),
        (-1e+13, 3, True, ' -10.000T'),
        (-1e+14, 3, True, '-100.000T'),
        (-1e+15, 3, True, '  -1.000P'),
        (-1e+16, 3, True, ' -10.000P'),
        (-1e+17, 3, True, '-100.000P'),
        (-1e+18, 3, True, '  -1.000E'),
        (-1e+19, 3, True, ' -10.000E'),
        (-1e+20, 3, True, '-100.000E'),
        (-1e+21, 3, True, '  -1.000Z'),
        (-1e+22, 3, True, ' -10.000Z'),
        (-1e+23, 3, True, '-100.000Z'),
        (-1e+24, 3, True, '  -1.000Y'),
        (-1e+25, 3, True, ' -10.000Y'),
        (-1e+26, 3, True, '-100.000Y'),
        (-1e+27, 3, True, '-999.999Y'),
        (-12.45, 1, True, ' -12.5 '),
        (-998.999e3, 1, True, '-999.0k'),
        (-998.999e3, 1, False, '-999.0k'),
        (-999.999e3, 1, True, '  -1.0M'),
        (-999.999e3, 1, DFLT, '  -1.0M'),
        (-999.999e3, 1, False, '-1.0M'),
        (-0.995, 0, False, '-995m'),
        (-0.9999, 0, False, '-1'),
        (-1.9999, 0, False, '-2'),
        (-999.99, 0, False, '-1k'),
        (-9.99, 1, False, '-10.0'),
        (-5.25e3, 1, True, '  -5.3k'),
        (-1.05e3, 0, True, '  -1k')
    ]
)
def test_peng(num, mant, rjust, ref):
    """ Test peng function behavior """
    obj = putil.eng.peng
    obj = obj if isdflt(rjust) else functools.partial(obj, rjust=rjust)
    assert obj(num, mant) == ref


@pytest.mark.eng
@pytest.mark.parametrize('arg', [None, 5, '', ' 5x', 'a5M', '- - a5M'])
@pytest.mark.parametrize(
    'func', [
        putil.eng.peng_float,
        putil.eng.peng_frac,
        putil.eng.peng_int,
        putil.eng.peng_mant,
        putil.eng.peng_power,
        putil.eng.peng_suffix,
    ]
)
def test_peng_snum_exceptions(func, arg):
    """
    Test exceptions of functions that receive a string representing
    a number in engineering notation
    """
    AE(func, dict(snum=arg), exmsg=sarg('snum'))


@pytest.mark.parametrize(
    'arg, ref', [
        (putil.eng.peng(5234.567, 3, True), 5.235e3),
        ('     5.235k    ', 5.235e3),
        ('    -5.235k    ', -5.235e3),
    ]
)
def test_peng_float(arg, ref):
    """ Test peng_float function behavior """
    assert putil.eng.peng_float(arg) == ref


@pytest.mark.parametrize(
    'arg, ref', [
        (putil.eng.peng(5234.567, 6, True), 234567),
        (putil.eng.peng(5234, 0, True), 0)
    ]
)
def test_peng_frac(arg, ref):
    """ Test peng_frac function behavior """
    assert putil.eng.peng_frac(arg) == ref


def test_peng_int():
    """ Test peng_int function behavior """
    assert putil.eng.peng_int(putil.eng.peng(5234.567, 6, True)) == 5


def test_peng_mant():
    """ Test peng_mant function behavior """
    assert putil.eng.peng_mant(putil.eng.peng(5234.567, 3, True)) == 5.235


def test_peng_power():
    """ Test peng_power function behavior """
    tup = putil.eng.peng_power(putil.eng.peng(1234.567, 3, True))
    assert tup == ('k', 1000.0)
    assert isinstance(tup[1], float)


@pytest.mark.parametrize(
    'arg, ref', [
        (putil.eng.peng(1, 3, True), ' '),
        (putil.eng.peng(-10.5e-6, 3, False), 'u')
    ]
)
def test_peng_suffix(arg, ref):
    """ Test peng_suffix function behavior """
    assert putil.eng.peng_suffix(arg) == ref


@pytest.mark.eng
@pytest.mark.parametrize(
    'args, extype, name', [
        (dict(suffix='X', offset=-1), RuntimeError, 'suffix'),
        (dict(suffix='M', offset='a'), RuntimeError, 'offset'),
        (dict(suffix='M', offset=20), ValueError, 'offset'),
    ]
)
@pytest.mark.eng
def test_peng_suffix_math_exceptions(args, extype, name):
    """ Test peng_suffix_math function exceptions """
    putil.test.assert_exception(
        putil.eng.peng_suffix_math, args, extype, sarg(name)
    )


@pytest.mark.parametrize('args, ref', [((' ', 3), 'G'), (('u', -2), 'p')])
def test_peng_suffix_math(args, ref):
    """ Test peng_suffix_math function behavior """
    assert putil.eng.peng_suffix_math(*args) == ref


@pytest.mark.parametrize(
    'num, frac_length, exp_length, sign_always, ref', [
        ('5.35E+3', DFLT, DFLT, DFLT, '5.35E+3'),
        (0, DFLT, DFLT, DFLT, '0E+0'),
        (0.1, DFLT, DFLT, DFLT, '1E-1'),
        (0.01, DFLT, DFLT, DFLT, '1E-2'),
        (0.001, DFLT, DFLT, DFLT, '1E-3'),
        (0.00101, DFLT, DFLT, DFLT, '1.01E-3'),
        (0.123456789012, DFLT, DFLT, DFLT, '1.23456789012E-1'),
        (1234567.89012, DFLT, DFLT, DFLT, '1.23456789012E+6'),
        (1, DFLT, DFLT, DFLT, '1E+0'),
        (20, DFLT, DFLT, DFLT, '2E+1'),
        (100, DFLT, DFLT, DFLT, '1E+2'),
        (200, DFLT, DFLT, DFLT, '2E+2'),
        (333, DFLT, DFLT, DFLT, '3.33E+2'),
        (4567, DFLT, DFLT, DFLT, '4.567E+3'),
        (4567.890, DFLT, DFLT, DFLT, '4.56789E+3'),
        (500, 3, DFLT, DFLT, '5.000E+2'),
        (4567.890, 8, DFLT, DFLT, '4.56789000E+3'),
        (99.999, 1, DFLT, DFLT, '1.0E+2'),
        (4567.890, DFLT, DFLT, True, '+4.56789E+3'),
        (500, 3, DFLT, True, '+5.000E+2'),
        (4567.890, 8, DFLT, True, '+4.56789000E+3'),
        (99.999, 1, DFLT, True, '+1.0E+2'),
        (500, 3, 2, True, '+5.000E+02'),
        (4567.890, 8, 3, True, '+4.56789000E+003'),
        (9999999999.999, 1, 1, True, '+1.0E+10'),
        (-0.1, DFLT, DFLT, DFLT, '-1E-1'),
        (-0.01, DFLT, DFLT, DFLT, '-1E-2'),
        (-0.001, DFLT, DFLT, DFLT, '-1E-3'),
        (-0.00101, DFLT, DFLT, DFLT, '-1.01E-3'),
        (-0.123456789012, DFLT, DFLT, DFLT, '-1.23456789012E-1'),
        (-1234567.89012, DFLT, DFLT, DFLT, '-1.23456789012E+6'),
        (-1, DFLT, DFLT, DFLT, '-1E+0'),
        (-20, DFLT, DFLT, DFLT, '-2E+1'),
        (-100, DFLT, DFLT, DFLT, '-1E+2'),
        (-200, DFLT, DFLT, DFLT, '-2E+2'),
        (-333, DFLT, DFLT, DFLT, '-3.33E+2'),
        (-4567, DFLT, DFLT, DFLT, '-4.567E+3'),
        (-4567.890, DFLT, DFLT, DFLT, '-4.56789E+3'),
        (-500, 3, DFLT, DFLT, '-5.000E+2'),
        (-4567.890, 8, DFLT, DFLT, '-4.56789000E+3'),
        (-99.999, 1, DFLT, DFLT, '-1.0E+2'),
        (-4567.890, DFLT, DFLT, True, '-4.56789E+3'),
        (-500, 3, DFLT, True, '-5.000E+2'),
        (-4567.890, 8, DFLT, True, '-4.56789000E+3'),
        (-99.999, 1, DFLT, True, '-1.0E+2'),
        (-500, 3, 2, True, '-5.000E+02'),
        (-4567.890, 8, 3, True, '-4.56789000E+003'),
        (-9999999999.999, 1, 1, True, '-1.0E+10'),
    ]
)
def test_to_scientific_string(num, frac_length, exp_length, sign_always, ref):
    """ Test _to_scientific function behavior """
    fp = functools.partial
    obj = putil.eng.to_scientific_string
    obj = obj if isdflt(frac_length) else fp(obj, frac_length=frac_length)
    obj = obj if isdflt(exp_length) else fp(obj, exp_length=exp_length)
    obj = obj if isdflt(sign_always) else fp(obj, sign_always=sign_always)
    assert obj(num) == ref


CVECTOR = [-1+2j, 3+4j, 5+6j, 7+8j, 9-10j, 11+12j, -13+14j, 15678-16j]
@pytest.mark.parametrize(
    'vector, args, ref, header', [
        (
            None,
            DFLT,
            'None',
            ''
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            DFLT,
            '[ 1, 2, 3, 4, 5, 6, 7, 8 ]',
            ''
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            dict(indent=20),
            '[ 1, 2, 3, 4, 5, 6, 7, 8 ]',
            ''
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            dict(indent=20),
            '[ 1, 2, 3, 4, 5, 6, 7, 8 ]',
            ''
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            dict(limit=True),
            '[ 1, 2, 3, ..., 6, 7, 8 ]',
            ''
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            dict(limit=True, indent=20),
            '[ 1, 2, 3, ..., 6, 7, 8 ]',
            ''
        ),
        # Float and integer item    #ref = (
        (
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            dict(eng=True),
            '[    1.000m,   20.000u,  300.000M,    4.000p,'
            '    5.250k,   -6.000n,  700.000 ,  800.000m ]',
            ''
        ),
        (
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            dict(eng=True, indent=20),
            '[    1.000m,   20.000u,  300.000M,    4.000p,'
            '    5.250k,   -6.000n,  700.000 ,  800.000m ]',
            ''
        ),
        (
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            dict(limit=True, eng=True),
            '[    1.000m,   20.000u,  300.000M,'
            ' ...,'
            '   -6.000n,  700.000 ,  800.000m ]',
            ''
        ),
        (
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            dict(limit=True, eng=True, indent=20),
            '[    1.000m,   20.000u,  300.000M,'
            ' ...,'
            '   -6.000n,  700.000 ,  800.000m ]',
            ''
        ),
        (
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            dict(eng=True, frac_length=1),
            '[    1.0m,   20.0u,  300.0M,    4.0p,'
            '    5.3k,   -6.0n,  700.0 ,  800.0m ]',
            ''
        ),
        (
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            dict(eng=True, frac_length=1, indent=20),
            '[    1.0m,   20.0u,  300.0M,    4.0p,'
            '    5.3k,   -6.0n,  700.0 ,  800.0m ]',
            ''
        ),
        (
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            dict(limit=True, eng=True, frac_length=1),
            '[    1.0m,   20.0u,  300.0M, ...,   -6.0n,  700.0 ,  800.0m ]',
            ''
        ),
        (
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            dict(limit=True, indent=20, eng=True, frac_length=1),
            '[    1.0m,   20.0u,  300.0M, ...,   -6.0n,  700.0 ,  800.0m ]',
            ''
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            dict(width=8),
            #12345678
            '[ 1, 2,\n'
            '  3, 4,\n'
            '  5, 6,\n'
            '  7, 8 ]',
            ''
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            dict(width=10),
            '[ 1, 2, 3,\n'
            '  4, 5, 6,\n'
            '  7, 8 ]',
            ''
        ),
        (
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 8, 9],
            dict(width=20, eng=True, frac_length=0),
            '[    1m,   20u,\n'
            '   300M,    4p,\n'
            '     5k,   -6n,\n'
            '   700 ,    8 ,\n'
            '     9  ]',
            ''
        ),
        (
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            dict(width=30, eng=True, frac_length=1),
            '[    1.0m,   20.0u,  300.0M,\n'
            '     4.0p,    5.3k,   -6.0n,\n'
            '   700.0 ,  800.0m ]',
            ''
        ),
        (
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 8, 9],
            dict(width=20, eng=True, frac_length=0, limit=True),
            '[    1m,\n'
            '    20u,\n'
            '   300M,\n'
            '   ...\n'
            '   700 ,\n'
            '     8 ,\n'
            '     9  ]',
            ''
        ),
        (
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 8, 9],
            dict(width=30, eng=True, frac_length=1, limit=True),
            '[    1.0m,   20.0u,  300.0M,\n'
            '             ...\n'
            '   700.0 ,    8.0 ,    9.0  ]',
            ''
        ),
        (
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 8, 9],
            dict(width=30, eng=True, frac_length=1, limit=True, indent=8),
            'Vector: [    1.0m,   20.0u,  300.0M,\n'
            '                     ...\n'
            '           700.0 ,    8.0 ,    9.0  ]',
            'Vector: '
        ),
        (
            [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 0.8],
            dict(width=30, eng=True, frac_length=1, indent=8),
            'Vector: [    1.0m,   20.0u,  300.0M,\n'
            '             4.0p,    5.3k,   -6.0n,\n'
            '           700.0 ,  800.0m ]',
            'Vector: '
        ),
        (
            [
                1.23456789, 2.45678901, 3.45678901, 4.56789012,
                5.67890123, 6.78901234, 7.89012345
            ],
            dict(limit=True, width=80-22, indent=22),
            'Independent variable: [ 1.23456789, 2.45678901, 3.45678901,\n'
            '                                        ...\n'
            '                        5.67890123, 6.78901234, 7.89012345 ]',
            'Independent variable: '
        ),
        (
            [
                1.23456789, 2.45678901, 3.45678901, 4.56789012,
                5.67890123, 6.78901234, 7.89012345
            ],
            dict(width=49, indent=17),
            'Independent var: [ 1.23456789, 2.45678901, 3.45678901, '
            '4.56789012,\n'
            '                   5.67890123, 6.78901234, 7.89012345 ]',
            'Independent var: '
        ),
        # Complex items
        (
            CVECTOR,
            DFLT,
            '[ -1+2j, 3+4j, 5+6j, 7+8j, 9-10j, 11+12j, -13+14j, 15678-16j ]',
            ''
        ),
        (
            CVECTOR,
            dict(indent=20),
            '[ -1+2j, 3+4j, 5+6j, 7+8j, 9-10j, 11+12j, -13+14j, 15678-16j ]',
            ''
        ),
        (
            CVECTOR,
            dict(limit=True),
            '[ -1+2j, 3+4j, 5+6j, ..., 11+12j, -13+14j, 15678-16j ]',
            ''
        ),
        (
            CVECTOR,
            dict(limit=True, indent=20),
            '[ -1+2j, 3+4j, 5+6j, ..., 11+12j, -13+14j, 15678-16j ]',
            ''
        ),
        (
            CVECTOR,
            dict(eng=True),
            '[   -1.000 +   2.000 j,    3.000 +   4.000 j,'
            '    5.000 +   6.000 j,'
            '    7.000 +   8.000 j,    9.000 -  10.000 j,'
            '   11.000 +  12.000 j,'
            '  -13.000 +  14.000 j,   15.678k-  16.000 j ]',
            ''
        ),
        (
            CVECTOR,
            dict(eng=True, indent=20),
            '[   -1.000 +   2.000 j,    3.000 +   4.000 j,'
            '    5.000 +   6.000 j,'
            '    7.000 +   8.000 j,    9.000 -  10.000 j,'
            '   11.000 +  12.000 j,'
            '  -13.000 +  14.000 j,   15.678k-  16.000 j ]',
            ''
        ),
        (
            CVECTOR,
            dict(limit=True, eng=True),
            '[   -1.000 +   2.000 j,    3.000 +   4.000 j,'
            '    5.000 +   6.000 j,'
            ' ...,   11.000 +  12.000 j,  -13.000 +  14.000 j,'
            '   15.678k-  16.000 j ]',
            ''
        ),
        (
            CVECTOR,
            dict(limit=True, eng=True, indent=20),
            '[   -1.000 +   2.000 j,    3.000 +   4.000 j,'
            '    5.000 +   6.000 j,'
            ' ...,   11.000 +  12.000 j,  -13.000 +  14.000 j,'
            '   15.678k-  16.000 j ]',
            ''
        ),
        (
            CVECTOR,
            dict(eng=True, frac_length=1),
            '[   -1.0 +   2.0 j,    3.0 +   4.0 j,    5.0 +   6.0 j,'
            '    7.0 +   8.0 j,    9.0 -  10.0 j,   11.0 +  12.0 j,'
            '  -13.0 +  14.0 j,   15.7k-  16.0 j ]',
            ''
        ),
        (
            CVECTOR,
            dict(eng=True, frac_length=1, indent=20),
            '[   -1.0 +   2.0 j,    3.0 +   4.0 j,    5.0 +   6.0 j,'
            '    7.0 +   8.0 j,    9.0 -  10.0 j,   11.0 +  12.0 j,'
            '  -13.0 +  14.0 j,   15.7k-  16.0 j ]',
            ''
        ),
        (
            CVECTOR,
            dict(limit=True, eng=True, frac_length=1),
            '[   -1.0 +   2.0 j,    3.0 +   4.0 j,    5.0 +   6.0 j,'
            ' ...,   11.0 +  12.0 j,  -13.0 +  14.0 j,   15.7k-  16.0 j ]',
            ''
        ),
        (
            CVECTOR,
            dict(limit=True, eng=True, frac_length=1, indent=20),
            '[   -1.0 +   2.0 j,    3.0 +   4.0 j,    5.0 +   6.0 j,'
            ' ...,   11.0 +  12.0 j,  -13.0 +  14.0 j,   15.7k-  16.0 j ]',
            ''
        ),
        (
            CVECTOR,
            dict(width=22),
            '[ -1+2j, 3+4j, 5+6j,\n'
            '  7+8j, 9-10j, 11+12j,\n'
            '  -13+14j, 15678-16j ]',
            ''
        ),
        (
            CVECTOR,
            dict(width=20),
            '[ -1+2j, 3+4j, 5+6j,\n'
            '  7+8j, 9-10j,\n'
            '  11+12j, -13+14j,\n'
            '  15678-16j ]',
            ''
        ),
        (
            CVECTOR,
            dict(width=29, eng=True, frac_length=0),
            '[   -1 +   2 j,    3 +   4 j,\n'
            '     5 +   6 j,    7 +   8 j,\n'
            '     9 -  10 j,   11 +  12 j,\n'
            '   -13 +  14 j,   16k-  16 j ]',
            ''
        ),
        (
            CVECTOR,
            dict(width=37, eng=True, frac_length=1),
            '[   -1.0 +   2.0 j,    3.0 +   4.0 j,\n'
            '     5.0 +   6.0 j,    7.0 +   8.0 j,\n'
            '     9.0 -  10.0 j,   11.0 +  12.0 j,\n'
            '   -13.0 +  14.0 j,   15.7k-  16.0 j ]',
            ''
        ),
        (
            CVECTOR,
            dict(width=16, eng=True, frac_length=0),
            '[   -1 +   2 j,\n'
            '     3 +   4 j,\n'
            '     5 +   6 j,\n'
            '     7 +   8 j,\n'
            '     9 -  10 j,\n'
            '    11 +  12 j,\n'
            '   -13 +  14 j,\n'
            '    16k-  16 j ]',
            ''
        ),
        (
            CVECTOR,
            dict(width=16, eng=True, frac_length=0, limit=True),
            '[   -1 +   2 j,\n'
            '     3 +   4 j,\n'
            '     5 +   6 j,\n'
            '       ...\n'
            '    11 +  12 j,\n'
            '   -13 +  14 j,\n'
            '    16k-  16 j ]',
            ''
        ),
        (
            CVECTOR,
            dict(width=56, eng=True, frac_length=1, limit=True),
            '[   -1.0 +   2.0 j,    3.0 +   4.0 j,    5.0 +   6.0 j,\n'
            '                           ...\n'
            '    11.0 +  12.0 j,  -13.0 +  14.0 j,   15.7k-  16.0 j ]',
            ''
        ),
        (
            CVECTOR,
            dict(width=64, eng=True, frac_length=1, limit=True, indent=8),
            'Vector: [   -1.0 +   2.0 j,    3.0 +   4.0 j,    5.0 +   6.0 j,\n'
            '                                   ...\n'
            '            11.0 +  12.0 j,  -13.0 +  14.0 j,   15.7k-  16.0 j ]',
            'Vector: '
        ),
        (
            CVECTOR,
            dict(width=20, indent=8),
            'Vector: [ -1+2j, 3+4j, 5+6j,\n'
            '          7+8j, 9-10j,\n'
            '          11+12j, -13+14j,\n'
            '          15678-16j ]',
            'Vector: '
        ),
        (
            CVECTOR,
            dict(width=30, indent=8, limit=True),
            'Vector: [ -1+2j, 3+4j, 5+6j,\n'
            '                 ...\n'
            '          11+12j, -13+14j, 15678-16j ]',
            'Vector: '
        ),
        (
            CVECTOR,
            dict(width=20, indent=8, limit=True),
            'Vector: [ -1+2j,\n'
            '          3+4j,\n'
            '          5+6j,\n'
            '           ...\n'
            '          11+12j,\n'
            '          -13+14j,\n'
            '          15678-16j ]',
            'Vector: '
        ),
        (
            array(
                [
                    -0.10081675027325637-0.06910517142735251j,
                    0.018754229185649937+0.017142783560861786j,
                    0+18j
                ]
            ),
            DFLT,
            '[ -0.100816750273-0.0691051714274j, '
            '0.0187542291856+0.0171427835609j, 18j ]',
            ''
        ),
        (
            array(
                [
                    -0.10081675027325637-0.06910517142735251j,
                    0.018754229185649937+0.017142783560861786j,
                    0+18j
                ]
            ),
            dict(width=60, limit=True, indent=20),
            'Dependent variable: [ -0.100816750273-0.0691051714274j,\n'
            '                      0.0187542291856+0.0171427835609j, 18j ]',
            'Dependent variable: '
        ),
        (
            array(
                [
                    -0.10081675027325637-0.06910517142735251j,
                    0.018754229185649937+0.017142783560861786j,
                    0+18j,
                    0.118754229185649937+0.117142783560861786j,
                    0.218754229185649937+0.217142783560861786j,
                    0+28j,
                    10+2j,
                ]
            ),
            dict(width=60),
            '[ -0.100816750273-0.0691051714274j,\n'
            '  0.0187542291856+0.0171427835609j, 18j,\n'
            '  0.118754229186+0.117142783561j,\n'
            '  0.218754229186+0.217142783561j, 28j, 10+2j ]',
            ''
        ),
        (
            array(
                [
                    -0.10081675027325637-0.06910517142735251j,
                    0.018754229185649937+0.017142783560861786j,
                    0+18j,
                    0.118754229185649937+0.117142783560861786j,
                    0.218754229185649937+0.217142783560861786j,
                    0+28j,
                    10+2j,
                ]
            ),
            dict(width=60, limit=True),
            '[ -0.100816750273-0.0691051714274j,\n'
            '  0.0187542291856+0.0171427835609j,\n'
            '  18j,\n'
            '                 ...\n'
            '  0.218754229186+0.217142783561j,\n'
            '  28j,\n'
            '  10+2j ]',
            ''
        ),
    ]
)
def test_pprint_vector(vector, args, ref, header):
    """ Test pprint_vector function behavior """
    obj = putil.eng.pprint_vector
    obj = obj if isdflt(args) else functools.partial(obj, **args)
    assert header+obj(vector) == ref


@pytest.mark.parametrize(
    'args', [
        dict(
            vector=[1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 8, 9],
            width=5, eng=True, frac_length=1, limit=True
        ),
        dict(
            vector=[-1+2j, 3, 5+6j, 7+8j, 9-10j, 11+12j, -13+14j, 15678-16j],
            width=8, limit=True
        )
    ]
)
@pytest.mark.eng
def test_pprint_vector_exceptions(args):
    """ Test pprint_vector function exceptions """
    msg = 'Argument `width` is too small'
    putil.test.assert_exception(putil.eng.pprint_vector, args, ValueError, msg)


@pytest.mark.parametrize(
    'num, dec, ref', [
        (None, DFLT, None),
        (1.3333, 2, 1.33),
        (1.5555E-12, 2, 1.56E-12),
        (3, 2, 3),
        (array([1.3333, 2.666666]), 2, array([1.33, 2.67])),
        (array([1.3333E-12, 2.666666E-12]), 2, array([1.33E-12, 2.67E-12])),
        (array([1, 3]), 2, array([1, 3])),
    ]
)
def test_round_mantissa(num, dec, ref):
    """ Test round_mantissa function behavior """
    obj = putil.eng.round_mantissa
    obj = obj if isdflt(dec) else functools.partial(obj, decimals=dec)
    test = obj(num) == ref
    assert test.all() if isinstance(num, ndarray) else test
