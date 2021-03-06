from collections import namedtuple

from NeoVintageous.tests import unittest


test_data = namedtuple('test_data', 'initial_text regions cmd_params expected msg')

TESTS = (
    test_data('abc aaa100bbb abc', [[(0, 0), (0, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa110bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc', [[(0, 0), (0, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa-90bbb abc', ''),  # noqa: E241,E501

    test_data('abc aaa100bbb abc', [[(0, 8), (0, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa110bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc', [[(0, 8), (0, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa-90bbb abc', ''),  # noqa: E241,E501

    test_data('abc aaa100bbb abc\nabc aaa100bbb abc', [[(0, 0), (0, 0)], [(1, 0), (1, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa110bbb abc\nabc aaa110bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc\nabc aaa-100bbb abc', [[(0, 0), (0, 0)], [(1, 0), (1, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa-90bbb abc\nabc aaa-90bbb abc', ''),  # noqa: E241,E501

    test_data('abc aaa100bbb abc\nabc aaa100bbb abc', [[(0, 8), (0, 8)], [(1, 8), (1, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa110bbb abc\nabc aaa110bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc\nabc aaa-100bbb abc', [[(0, 0), (0, 0)], [(1, 8), (1, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa-90bbb abc\nabc aaa-90bbb abc', ''),  # noqa: E241,E501

    test_data('abc aaa100bbb abc', [[(0, 0), (0, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa90bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc', [[(0, 0), (0, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa-110bbb abc', ''),  # noqa: E241,E501

    test_data('abc aaa100bbb abc', [[(0, 8), (0, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa90bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc', [[(0, 8), (0, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa-110bbb abc', ''),  # noqa: E241,E501

    test_data('abc aaa100bbb abc\nabc aaa100bbb abc', [[(0, 0), (0, 0)], [(1, 0), (1, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa90bbb abc\nabc aaa90bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc\nabc aaa-100bbb abc', [[(0, 0), (0, 0)], [(1, 0), (1, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa-110bbb abc\nabc aaa-110bbb abc', ''),  # noqa: E241,E501

    test_data('abc aaa100bbb abc\nabc aaa100bbb abc', [[(0, 8), (0, 8)], [(1, 8), (1, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa90bbb abc\nabc aaa90bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc\nabc aaa-100bbb abc', [[(0, 0), (0, 0)], [(1, 8), (1, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa-110bbb abc\nabc aaa-110bbb abc', ''),  # noqa: E241,E501

    # TODO: Test with sels on same line.
    # TODO: Test with standalone number.
    # TODO: Test with number followed by suffix.
)


class Test__vi_ctrl_x(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            # TODO: Perhaps we should ensure that other state is reset too?
            self.write(data.initial_text)
            self.select([self._R(*region) for region in data.regions])

            self.view.run_command('_vi_modify_numbers', data.cmd_params)

            self.assertEqual(data.expected, self.content(), "[{0}] {1}".format(i, data.msg))
