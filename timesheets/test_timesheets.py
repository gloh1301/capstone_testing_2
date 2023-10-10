import unittest
from unittest import TestCase
from unittest.mock import patch, call

import timesheets

class TestTimeSheet(TestCase):

    """ mock input() and force return a value """

    @patch('builtins.input', side_effect=['2'])
    def test_get_hours_for_day(self, mock_input):
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(2, hours)

    @patch('builtins.input', side_effect=['cat', '', 'fish', '123bird', 'pizza123', '2'])
    def test_get_hours_for_day_non_numeric_rejected(self, mock_input):
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(2, hours)

    @patch('builtins.input', side_effect=['-1', '-1000', '6'])
    def test_get_hours_for_day_hours_greater_than_zero(self, mock_input):
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(6, hours)

    @patch('builtins.input', side_effect=['24.000001', '25', '1000', '9'])
    def test_get_hours_for_day_hours_less_than_24(self, mock_input):
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(9, hours)

    @patch('builtins.print')
    def test_display_total(self, mock_print):
        timesheets.display_total(1234)
        mock_print.assert_called_once_with('Total hours worked: 1234')

    @patch('timesheets.alert')
    def test_alert_meet_min_hours_doesnt_meet(self, mock_alert):
        timesheets.alert_not_meet_min_hours(12, 30)
        mock_alert.assert_called_once()

    @patch('timesheets.alert')
    def test_alert_meet_min_hours_does_meet_min(self, mock_alert):
        timesheets.alert_not_meet_min_hours(40, 30)
        mock_alert.assert_not_called()

    @patch('timesheets.get_hours_for_day')
    def test_get_hours(self, mock_get_hours):
        mock_hours = [5, 7, 9]
        mock_get_hours.side_effect = mock_hours
        days = ['m', 't', 'w']
        expected_hours = dict(zip(days, mock_hours))
        hours = timesheets.get_hours(days)
        self.assertEqual(expected_hours, hours)

    @patch('builtins.print')
    def test_display_hours(self, mock_print):
        example = {'M': 3, 'T': 12, 'W': 8.5}
        expected_table_calls = [
            call('Day            Hours Worked   '),
            call('M              3              '),
            call('T              12             '),
            call('W              8.5            ')
        ]
        timesheets.display_hours(example)
        mock_print.assert_has_calls(expected_table_calls)

    def test_total_hours(self):
        example = {'M': 3, 'T': 12, 'W': 8.5}
        total = timesheets.total_hours(example)
        expected_total = 3 + 12 + 8.5
        self.assertEqual(total, expected_total)

if __name__ == '__main__':
    unittest.main()