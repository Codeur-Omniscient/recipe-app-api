"""
Test module
"""
from django.test import SimpleTestCase
from app import calc


class CalcTests(SimpleTestCase):
    def test_add_numbers(self):
        """Test adding two numbers"""
        res = calc.add(1, 2)
        self.assertEqual(res, 3)
