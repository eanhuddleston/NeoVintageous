from NeoVintageous.tests import unittest


class Test__vi_star_InNormalMode(unittest.ViewTestCase):

    def test_select_match(self):
        self.write('abc\nabc')
        self.select(0)

        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('vi_search'), [self.Region(0, 3), self.Region(4, 7)])

    def test_select_match_middle(self):
        self.write('abc\nabc')
        self.select(1)

        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('vi_search'), [self.Region(0, 3), self.Region(4, 7)])

    def test_select_match_end(self):
        self.write('abc\nabc')
        self.select(2)

        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('vi_search'), [self.Region(0, 3), self.Region(4, 7)])

    def test_select_match_end2(self):
        self.write('abc\nabc')
        self.select(2)

        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('vi_search'), [self.Region(0, 3), self.Region(4, 7)])

    def test_select_repeat_match(self):
        self.write('abc\nabc\nfoo\nabc\nbar')
        self.select(0)

        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})
        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})

        self.assertSelection(12)
        self.assertEqual(self.view.get_regions('vi_search'), [
            self.Region(0, 3), self.Region(4, 7), self.Region(12, 15)])

    def test_select_wrap_match(self):
        self.write('boo\nabc\nfoo\nabc\nbar')
        self.select(12)

        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('vi_search'), [self.Region(4, 7), self.Region(12, 15)])

    def test_select_no_partial_match(self):
        self.write('boo\nabc\nabcxabc\nabc\nbar')
        self.select(4)

        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})

        self.assertSelection(16)
        self.assertEqual(self.view.get_regions('vi_search'), [self.Region(4, 7), self.Region(16, 19)])

    def test_select_no_match(self):
        self.write('boo\nabc\nfoo\nabc\nbar')
        self.select(9)

        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})

        self.assertSelection(8)
        self.assertEqual(self.view.get_regions('vi_search'), [self.Region(8, 11)])
