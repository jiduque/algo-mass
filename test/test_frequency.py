import unittest

from dat_mass.frequency import boyer_more


class TestFrequency(unittest.TestCase):
    def test_valid_majority(self):
        x = [4, 5, 5, 4, 6, 4, 4]
        y = 4
        f_x = boyer_more(x)
        self.assertEqual(y, f_x)

    def test_almost_majority(self):
        x = [3, 3, 5, 5, 5, 4]
        y = 4
        f_x = boyer_more(x)
        self.assertEqual(y, f_x)


if __name__ == '__main__':
    unittest.main()
