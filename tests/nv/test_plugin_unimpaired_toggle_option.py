from NeoVintageous.tests import unittest

from NeoVintageous.nv.plugin_unimpaired import _set_bool_option
from NeoVintageous.nv.plugin_unimpaired import _set_value_option
from NeoVintageous.nv.plugin_unimpaired import _list_option
from NeoVintageous.nv.plugin_unimpaired import _minimap_option


class TestToggleOption(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.line_numbers = self.settings().get('line_numbers')
        self.draw_white_space = self.settings().get('draw_white_space')
        self.minimap_visible = self.view.window().is_minimap_visible()

    def tearDown(self):
        self.settings().set('line_numbers', self.line_numbers)
        self.settings().set('draw_white_space', self.draw_white_space)
        self.view.window().set_minimap_visible(self.minimap_visible)
        super().tearDown()

    def test_set_bool_option(self):
        _set_bool_option(self.view, 'line_numbers', True)
        self.assertTrue(self.settings().get('line_numbers'))

        _set_bool_option(self.view, 'line_numbers', False)
        self.assertFalse(self.settings().get('line_numbers'))

        _set_bool_option(self.view, 'line_numbers', True)
        self.assertTrue(self.settings().get('line_numbers'))

        _set_bool_option(self.view, 'line_numbers')
        self.assertFalse(self.settings().get('line_numbers'))

        _set_bool_option(self.view, 'line_numbers')
        self.assertTrue(self.settings().get('line_numbers'))

    def test_set_value_option(self):
        _set_value_option(self.view, 'draw_white_space', 'all', 'selection', True)
        self.assertEqual('all', self.settings().get('draw_white_space'))

        _set_value_option(self.view, 'draw_white_space', 'all', 'selection', False)
        self.assertEqual('selection', self.settings().get('draw_white_space'))

        _set_value_option(self.view, 'draw_white_space', 'all', 'selection', True)
        self.assertEqual('all', self.settings().get('draw_white_space'))

        _set_value_option(self.view, 'draw_white_space', 'all', 'selection')
        self.assertEqual('selection', self.settings().get('draw_white_space'))

        _set_value_option(self.view, 'draw_white_space', 'all', 'selection')
        self.assertEqual('all', self.settings().get('draw_white_space'))

    def test_list_option(self):
        _list_option(self.view, True)
        self.assertEqual('all', self.settings().get('draw_white_space'))

        _list_option(self.view, False)
        self.assertEqual('selection', self.settings().get('draw_white_space'))

        _list_option(self.view, True)
        self.assertEqual('all', self.settings().get('draw_white_space'))

        _list_option(self.view)
        self.assertEqual('selection', self.settings().get('draw_white_space'))

        _list_option(self.view)
        self.assertEqual('all', self.settings().get('draw_white_space'))

    def test_minimap_option(self):
        _minimap_option(self.view, True)
        self.assertTrue(self.view.window().is_minimap_visible())

        _minimap_option(self.view, False)
        self.assertFalse(self.view.window().is_minimap_visible())

        _minimap_option(self.view, True)
        self.assertTrue(self.view.window().is_minimap_visible())

        _minimap_option(self.view)
        self.assertFalse(self.view.window().is_minimap_visible())

        _minimap_option(self.view)
        self.assertTrue(self.view.window().is_minimap_visible())
