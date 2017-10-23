from collections import namedtuple

from NeoVintageous.tests.utils import ViewTestCase


test_data = namedtuple('test_data', 'text startRegion findChar mode expectedRegion msg')


class F():

    def test_f(self):
        for (i, data) in enumerate(self.cases):
            self.write(data.text)
            self.select(self._R(*data.startRegion))

            self.view.run_command('_vi_find_in_line', {
                'mode': data.mode,
                'count': 1,
                'char': data.findChar,
                'inclusive': True
            })

            self._assertRegionsEqual(
                self._R(*data.expectedRegion),
                self.view.sel()[0],
                "Failed on index {} {} : Text:\"{}\" Region:{} Find:'{}'"
                .format(i, data.msg, data.text, data.startRegion, data.findChar)
            )


class Normal(F, ViewTestCase):
    cases = (
        test_data('0a23x5', (1, 1), 'x', ViewTestCase.NORMAL_MODE, (4, 4), 'Find ahead'),
        test_data('0ax345', (1, 1), 'x', ViewTestCase.NORMAL_MODE, (2, 2), 'Find next'),
        test_data('0x2345', (1, 1), 'x', ViewTestCase.NORMAL_MODE, (1, 1), 'Find self'),
        test_data('0a2xx5', (1, 1), 'x', ViewTestCase.NORMAL_MODE, (3, 3), 'Find multiple'),
        test_data('0x2x45', (1, 1), 'x', ViewTestCase.NORMAL_MODE, (3, 3), 'Find self multiple'),
        test_data('0a23:5', (1, 1), ':', ViewTestCase.NORMAL_MODE, (4, 4), 'Find ahead (colon)'),
        test_data('0a:345', (1, 1), ':', ViewTestCase.NORMAL_MODE, (2, 2), 'Find next (colon)'),
        test_data('0:2345', (1, 1), ':', ViewTestCase.NORMAL_MODE, (1, 1), 'Find self (colon)'),
        test_data('0a2::5', (1, 1), ':', ViewTestCase.NORMAL_MODE, (3, 3), 'Find multiple (colon)'),
        test_data('0:2:45', (1, 1), ':', ViewTestCase.NORMAL_MODE, (3, 3), 'Find self multiple (colon)'),
    )


class InternalNormal(F, ViewTestCase):
    cases = (
        test_data('0a23x5', (1, 1), 'x', ViewTestCase.INTERNAL_NORMAL_MODE, (1, 5), 'Find ahead'),
        test_data('0ax345', (1, 1), 'x', ViewTestCase.INTERNAL_NORMAL_MODE, (1, 3), 'Find next'),
        test_data('0x2345', (1, 1), 'x', ViewTestCase.INTERNAL_NORMAL_MODE, (1, 1), 'Find self'),
        test_data('0a2xx5', (1, 1), 'x', ViewTestCase.INTERNAL_NORMAL_MODE, (1, 4), 'Find multiple'),
        test_data('0x2x45', (1, 1), 'x', ViewTestCase.INTERNAL_NORMAL_MODE, (1, 4), 'Find self multiple'),
    )


class VisualMultiCharacter(F, ViewTestCase):
    cases = (
        test_data('0ab3x5', (1, 3), 'x', ViewTestCase.VISUAL_MODE, (1, 5), 'Forward'),
        test_data('0a23x5', (1, 5), 'x', ViewTestCase.VISUAL_MODE, (1, 5), 'Forward find b'),
        test_data('0b2xa5', (5, 1), 'x', ViewTestCase.VISUAL_MODE, (5, 3), 'Reverse no crossover'),
        test_data('0ba3x5', (3, 1), 'x', ViewTestCase.VISUAL_MODE, (2, 5), 'Reverse crossover'),
        test_data('0b2x45', (4, 1), 'x', ViewTestCase.VISUAL_MODE, (4, 3), 'Reverse find a'),
        test_data('0x2a45', (4, 1), 'x', ViewTestCase.VISUAL_MODE, (4, 1), 'Reverse find b'),
    )


class VisualSingleCharacter(F, ViewTestCase):
    cases = (
        test_data('ax', (0, 2), 'x', ViewTestCase.VISUAL_MODE, (0, 2), 'Forward find b'),
        test_data('bx', (2, 0), 'x', ViewTestCase.VISUAL_MODE, (2, 1), 'Reverse find a'),
        test_data('fx', (0, 1), 'x', ViewTestCase.VISUAL_MODE, (0, 2), 'Forward find next'),
        test_data('rx', (1, 0), 'x', ViewTestCase.VISUAL_MODE, (0, 2), 'Reverse find next'),
        test_data('f', (0, 1), 'f', ViewTestCase.VISUAL_MODE, (0, 1), 'Forward find self'),
        test_data('r', (1, 0), 'r', ViewTestCase.VISUAL_MODE, (1, 0), 'Reverse find self'),
    )


class VisualMultipleMatches(F, ViewTestCase):
    cases = (
        test_data('0abxx5', (1, 3), 'x', ViewTestCase.VISUAL_MODE, (1, 4), 'Forward find first'),
        test_data('0axx45', (1, 3), 'x', ViewTestCase.VISUAL_MODE, (1, 4), 'Forward find b'),
        test_data('0bxx45', (3, 1), 'x', ViewTestCase.VISUAL_MODE, (3, 2), 'Reverse find a'),
        test_data('0bxx45', (4, 1), 'x', ViewTestCase.VISUAL_MODE, (4, 2), 'Reverse find a'),
        test_data('0xax45', (3, 1), 'x', ViewTestCase.VISUAL_MODE, (2, 4), 'Reverse find b'),
    )


class VisualMultipleLine(F, ViewTestCase):
    cases = (
        test_data('012\n456', (0, 5), '2', ViewTestCase.VISUAL_MODE, (0, 5), 'Select L1->L2, find on L1'),
        test_data('012\n456', (0, 5), '6', ViewTestCase.VISUAL_MODE, (0, 7), 'Select L1->L2, find on L2'),
        test_data('012\n456', (0, 4), '2', ViewTestCase.VISUAL_MODE, (0, 4), 'Select L1->LF, find on L1'),
        test_data('012\n456', (0, 4), '6', ViewTestCase.VISUAL_MODE, (0, 4), 'Select L1->LF, find on L2'),
        test_data('012\n456', (5, 0), '2', ViewTestCase.VISUAL_MODE, (5, 2), 'Select L2->L1, find on L1'),
        test_data('012\n456', (5, 0), '6', ViewTestCase.VISUAL_MODE, (5, 0), 'Select L2->L1, find on L2'),
        test_data('012\n456', (5, 3), '2', ViewTestCase.VISUAL_MODE, (5, 3), 'Select L2->LF, find on L1'),
        test_data('012\n456', (5, 3), '6', ViewTestCase.VISUAL_MODE, (5, 3), 'Select L2->LF, find on L2'),
        test_data('0123\n5678', (7, 5), '8', ViewTestCase.VISUAL_MODE, (6, 9), 'Select L2->LF+1, find on L2'),
    )
