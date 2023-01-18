import unittest
from unittest.mock import patch
from attendance_records.scr.project.main import main, make_dict


class TestMakeDict(unittest.TestCase):
    def setUp(self):
        self.id_crew = '052XL7D4'
        self.enter = [
            '052XL7D4 | 2020-01-01 08:55:54',
            '052XL7D4 | 2020-01-01 14:29:07'
        ]
        self.exit_f = [
            '052XL7D4 | 2020-01-01 13:28:18',
            '052XL7D4 | 2020-01-01 18:10:02'
        ]
        self.expected_lines = {
            '2020-01-01': [
                ['08:55:54', '13:28:18'],
                ['14:29:07', '18:10:02']
            ]
        }

    def test_normal_behaivor(self):
        self.assertEqual(make_dict(self.id_crew, self.enter, self.exit_f),
                         self.expected_lines)


class TestMain(unittest.TestCase):
    def setUp(self):
        self.id_crew = ['052XL7D4 | БОЙКО ВОЛОДИМИР ІВАНОВИЧ']
        self.enter = [
            '052XL7D4 | 2020-01-01 08:55:54',
            '052XL7D4 | 2020-01-01 14:29:07'
        ]
        self.exit_f = [
            '052XL7D4 | 2020-01-01 13:28:18',
            '052XL7D4 | 2020-01-01 18:10:02'
        ]
        self.expected_lines = {
            '052XL7D4': {
                'name': 'БОЙКО ВОЛОДИМИР ІВАНОВИЧ',
                'visits': {
                    '2020-01-01': [
                        ['08:55:54', '13:28:18'],
                        ['14:29:07', '18:10:02']
                    ]
                }
            }
        }

    @patch('attendance_records.scr.project.main.read_files')
    def test_namal_behaivor(self, mock_read_files):
        mock_read_files.return_value = (self.id_crew, self.enter, self.exit_f)
        res = main('')
        self.assertEqual(self.expected_lines, res)


if __name__ == '__main__ ':
    unittest.main()
