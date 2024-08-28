import unittest
from unittest.mock import patch, MagicMock
from utils import parse_arguments
import sys

class TestUtils(unittest.TestCase):

    @patch('sys.argv', ['main.py', '--output', 'test_output.mp4', '--duration', '20', '--interval', '0.2', '--format', 'mp4'])
    def test_parse_arguments(self):
        args = parse_arguments()

        self.assertEqual(args.output, 'test_output.mp4')
        self.assertEqual(args.duration, 20)
        self.assertEqual(args.interval, 0.2)
        self.assertEqual(args.format, 'mp4')

if __name__ == '__main__':
    unittest.main()
