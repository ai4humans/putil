# series.py
# Copyright (c) 2013-2015 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0103,C0111,F0401,R0201,R0903,W0201,W0212,W0232,W0621

from __future__ import print_function
import matplotlib
import numpy
import os
import pytest
import sys

import putil.plot
from .fixtures import compare_images, IMGTOL
sys.path.append('..')
from tests.plot.gen_ref_images import unittest_series_images


###
# Tests for Series
###
class TestSeries(object):
    """ Tests for Series """
    def test_data_source_wrong_type(self, default_source):
        """
        Test if object behaves correctly when checking the data_source argument
        """
        class TestSource(object):
            def __init__(self):
                pass
        # These assignments should raise an exception
        obj = putil.plot.BasicSource(
            indep_var=numpy.array([1, 2, 3, 4]),
            dep_var=numpy.array([10, 20, 30, 40])
        )
        obj._indep_var = None
        putil.test.assert_exception(
            putil.plot.Series,
            {'data_source':obj, 'label':'test'},
            RuntimeError,
            'Argument `data_source` is not fully specified'
        )
        putil.test.assert_exception(
            putil.plot.Series,
            {'data_source':5, 'label':'test'},
            RuntimeError,
            'Argument `data_source` does not have an `indep_var` attribute'
        )
        obj = TestSource()
        obj.indep_var = numpy.array([5, 6, 7, 8])
        putil.test.assert_exception(
            putil.plot.Series,
            {'data_source':obj, 'label':'test'},
            RuntimeError,
            'Argument `data_source` does not have an `dep_var` attribute'
        )
        # These assignments should not raise an exception
        obj.dep_var = numpy.array([0, -10, 5, 4])
        putil.plot.Series(data_source=None, label='test')
        putil.plot.Series(data_source=obj, label='test')
        obj = putil.plot.Series(data_source=default_source, label='test')
        assert (obj.indep_var == numpy.array([5, 6, 7, 8])).all()
        assert (obj.dep_var == numpy.array([0, -10, 5, 4])).all()

    def test_label_wrong_type(self, default_source):
        """ Test label data validation """
        # This assignments should raise an exception
        putil.test.assert_exception(
            putil.plot.Series,
            {'data_source':default_source, 'label':5},
            RuntimeError,
            'Argument `label` is not valid'
        )
        putil.plot.Series(data_source=default_source, label=None)
        obj = putil.plot.Series(data_source=default_source, label='test')
        assert obj.label == 'test'

    def test_color_wrong_type(self, default_source):
        """ Test color data validation """
        # This assignments should raise an exception
        putil.test.assert_exception(
            putil.plot.Series,
            {'data_source':default_source, 'label':'test', 'color':default_source},
            RuntimeError,
            'Argument `color` is not valid'
        )
        invalid_color_list = [
            'invalid_color_name',
            -0.01,
            1.1,
            '#ABCDEX',
            (-1, 1, 1),
            [1, 2, 0.5],
            [1, 1, 2],
            (-1, 1, 1, 1),
            [1, 2, 0.5, 0.5],
            [1, 1, 2, 1],
            (1, 1, 1, -1)
        ]
        valid_color_list = [
            None,
            'moccasin',
            0.5,
            '#ABCDEF',
            (0.5, 0.5, 0.5),
            [0.25, 0.25, 0.25, 0.25]
        ]
        for color in invalid_color_list:
            putil.test.assert_exception(
                putil.plot.Series,
                {'data_source':default_source, 'label':'test', 'color':color},
                TypeError,
                'Invalid color specification'
            )
        # These assignments should not raise an exception
        putil.plot.Series(data_source=default_source, label='test', color=None)
        for color in valid_color_list:
            obj = putil.plot.Series(
                data_source=default_source,
                label='test',
                color=color
            )
            assert obj.color == (color.lower() if isinstance(color, str) else color)

    def test_marker_wrong_type(self, default_source):
        """ Test marker data validation """
        # This assignments should raise an exception
        putil.test.assert_exception(
            putil.plot.Series,
            {'data_source':default_source, 'label':'test', 'marker':'hello'},
            RuntimeError,
            'Argument `marker` is not valid'
        )
        # These assignments should not raise an exception
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            marker=None
        )
        assert obj.marker == None
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            marker='D'
        )
        assert obj.marker == 'D'
        obj = putil.plot.Series(data_source=default_source, label='test')
        assert obj.marker == 'o'

    def test_interp_wrong_type(self, default_source):
        """ Test interp data validation """
        # These assignments should raise an exception
        putil.test.assert_exception(
            putil.plot.Series,
            {'data_source':default_source, 'label':'test', 'interp':5},
            RuntimeError,
            'Argument `interp` is not valid'
        )
        putil.test.assert_exception(
            putil.plot.Series,
            {'data_source':default_source, 'label':'test', 'interp':'NOT_AN_OPTION'},
            ValueError,
            "Argument `interp` is not one of ['STRAIGHT', 'STEP', 'CUBIC', "
            "'LINREG'] (case insensitive)"
        )
        source_obj = putil.plot.BasicSource(
            indep_var=numpy.array([5]),
            dep_var=numpy.array([0])
        )
        putil.test.assert_exception(
            putil.plot.Series,
            {'data_source':source_obj, 'label':'test', 'interp':'CUBIC'},
            ValueError,
            'At least 4 data points are needed for CUBIC interpolation'
        )
        # These assignments should not raise an exception
        putil.plot.Series(data_source=source_obj, label='test', interp='STRAIGHT')
        putil.plot.Series(data_source=source_obj, label='test', interp='STEP')
        putil.plot.Series(data_source=source_obj, label='test', interp='LINREG')
        putil.plot.Series(data_source=default_source, label='test', interp=None)
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            interp='straight'
        )
        assert obj.interp == 'STRAIGHT'
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            interp='StEp'
        )
        assert obj.interp == 'STEP'
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            interp='CUBIC'
        )
        assert obj.interp == 'CUBIC'
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            interp='linreg'
        )
        assert obj.interp == 'LINREG'
        obj = putil.plot.Series(
            data_source=default_source,
            label='test'
        )
        assert obj.interp == 'CUBIC'

    def test_line_style_wrong_type(self, default_source):
        """ Test line_style data validation """
        # These assignments should raise an exception
        putil.test.assert_exception(
            putil.plot.Series,
            {'data_source':default_source, 'label':'test', 'line_style':5},
            RuntimeError,
            'Argument `line_style` is not valid'
        )
        putil.test.assert_exception(
            putil.plot.Series,
            {'data_source':default_source, 'label':'test', 'line_style':'x'},
            ValueError,
            "Argument `line_style` is not one of ['-', '--', '-.', ':']"
        )
        # These assignments should not raise an exception
        putil.plot.Series(data_source=default_source, label='test', line_style=None)
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            line_style='-'
        )
        assert obj.line_style == '-'
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            line_style='--'
        )
        assert obj.line_style == '--'
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            line_style='-.'
        )
        assert obj.line_style == '-.'
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            line_style=':'
        )
        assert obj.line_style == ':'
        obj = putil.plot.Series(
            data_source=default_source,
            label='test'
        )
        assert obj.line_style == '-'

    def test_secondary_axis_wrong_type(self, default_source):
        """ Test secondary_axis data validation """
        # This assignments should raise an exception
        putil.test.assert_exception(
            putil.plot.Series,
            {'data_source':default_source, 'label':'test', 'secondary_axis':5},
            RuntimeError,
            'Argument `secondary_axis` is not valid'
        )
        # These assignments should not raise an exception
        putil.plot.Series(
            data_source=default_source,
            label='test',
            secondary_axis=None
        )
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            secondary_axis=False
        )
        assert not obj.secondary_axis
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            secondary_axis=True
        )
        assert obj.secondary_axis
        obj = putil.plot.Series(
            data_source=default_source,
            label='test'
        )
        assert not obj.secondary_axis

    def test_calculate_curve(self, default_source):
        """ Test that interpolated curve is calculated when appropriate """
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            interp=None
        )
        assert (obj.interp_indep_var, obj.interp_dep_var) == (None, None)
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            interp='STRAIGHT'
        )
        assert (obj.interp_indep_var, obj.interp_dep_var) == (None, None)
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            interp='STEP'
        )
        assert (obj.interp_indep_var, obj.interp_dep_var) == (None, None)
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            interp='CUBIC'
        )
        assert (obj.interp_indep_var, obj.interp_dep_var) != (None, None)
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            interp='LINREG'
        )
        assert (obj.interp_indep_var, obj.interp_dep_var) != (None, None)
        obj = putil.plot.Series(
            data_source=default_source,
            label='test'
        )
        assert (obj.interp_indep_var, obj.interp_dep_var) != (None, None)

    def test_scale_indep_var(self, default_source):
        """ Test that independent variable scaling works """
        obj = putil.plot.Series(
            data_source=default_source,
            label='test',
            interp=None
        )
        assert obj.scaled_indep_var is not None
        assert obj.scaled_dep_var is not None
        assert obj.scaled_interp_indep_var is None
        assert obj.scaled_interp_dep_var is None
        obj._scale_indep_var(2)
        obj._scale_dep_var(4)
        assert (obj.scaled_indep_var == numpy.array([2.5, 3.0, 3.5, 4.0])).all()
        assert (obj.scaled_dep_var == numpy.array([0.0, -2.5, 1.25, 1.0])).all()
        assert obj.scaled_interp_indep_var is None
        assert obj.scaled_interp_dep_var is None
        obj.interp = 'CUBIC'
        assert (obj.scaled_indep_var == numpy.array([2.5, 3.0, 3.5, 4.0])).all()
        assert (obj.scaled_dep_var == numpy.array([0.0, -2.5, 1.25, 1.0])).all()
        assert obj.scaled_interp_indep_var is not None
        assert obj.scaled_interp_dep_var is not None

    def test_str(self, default_source):
        """ Test that str behaves correctly """
        marker_list = [
            {
                'value':None,
                'string':'None'
            },
            {
                'value':'o',
                'string':'o'
            },
            {
                'value':matplotlib.path.Path([(0, 0), (1, 1)]),
                'string':'matplotlib.path.Path object'
            },
            {
                'value':[(0, 0), (1, 1)],
                'string':'[(0, 0), (1, 1)]'
            },
            {
                'value':r'$a_{b}$',
                'string':r'$a_{b}$'
            },
            {
                'value':matplotlib.markers.TICKLEFT,
                'string':'matplotlib.markers.TICKLEFT'
            }
        ]
        for marker_dict in marker_list:
            obj = putil.plot.Series(
                data_source=default_source,
                label='test',
                marker=marker_dict['value']
            )
            ret = (
                'Independent variable: [ 5.0, 6.0, 7.0, 8.0 ]\n'
                'Dependent variable: [ 0.0, -10.0, 5.0, 4.0 ]\n'
                'Label: test\n'
                'Color: k\n'
                'Marker: {0}\n'
                'Interpolation: CUBIC\n'
                'Line style: -\n'
                'Secondary axis: False'.format(marker_dict['string'])
            )
            if str(obj) != ret:
                print('Object:')
                print(str(obj))
                print('')
                print('Comparison:')
                print(ret)
            assert str(obj) == ret

    def test_cannot_delete_attributes(self, default_source):
        """ Test that del method raises an exception on all class attributes """
        obj = putil.plot.Series(data_source=default_source, label='test')
        with pytest.raises(AttributeError) as excinfo:
            del obj.data_source
        assert putil.test.get_exmsg(excinfo) == "can't delete attribute"
        with pytest.raises(AttributeError) as excinfo:
            del obj.label
        assert putil.test.get_exmsg(excinfo) == "can't delete attribute"
        with pytest.raises(AttributeError) as excinfo:
            del obj.color
        assert putil.test.get_exmsg(excinfo) == "can't delete attribute"
        with pytest.raises(AttributeError) as excinfo:
            del obj.marker
        assert putil.test.get_exmsg(excinfo) == "can't delete attribute"
        with pytest.raises(AttributeError) as excinfo:
            del obj.interp
        assert putil.test.get_exmsg(excinfo) == "can't delete attribute"
        with pytest.raises(AttributeError) as excinfo:
            del obj.line_style
        assert putil.test.get_exmsg(excinfo) == "can't delete attribute"
        with pytest.raises(AttributeError) as excinfo:
            del obj.secondary_axis
        assert putil.test.get_exmsg(excinfo) == "can't delete attribute"

    def test_images(self, tmpdir):
        """ Compare images to verify correct plotting of series """
        tmpdir.mkdir('test_images')
        images_dict_list = unittest_series_images(mode='test', test_dir=str(tmpdir))
        for images_dict in images_dict_list:
            ref_file_name = images_dict['ref_file_name']
            ref_ci_file_name = images_dict['ref_ci_file_name']
            test_file_name = images_dict['test_file_name']
            metrics = compare_images(ref_file_name, test_file_name)
            result = (metrics[0] < IMGTOL) and (metrics[1] < IMGTOL)
            metrics_ci = compare_images(ref_ci_file_name, test_file_name)
            result_ci = (metrics_ci[0] < IMGTOL) and (metrics_ci[1] < IMGTOL)
            if (not result) and (not result_ci):
                print('Images do not match')
                print('Reference image: file://{0}'.format(
                    os.path.realpath(ref_file_name)
                ))
                print('Reference CI image: file://{0}'.format(
                    os.path.realpath(ref_ci_file_name)
                ))
                print('Actual image: file://{0}'.format(
                    os.path.realpath(test_file_name)
                ))
            # print 'Comparison: {0} with {1} -> {2} {3}'.format(
            #   ref_file_name,
            #   test_file_name,
            #   result,
            #   metrics
            # )
            assert result or result_ci