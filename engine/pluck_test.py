import unittest
from pluck import pluck


class TestPluck(unittest.TestCase):
  def test_simple(self):
    arg = {'a': 1}
    result, _err = pluck(arg, 'a')
    expectation = 1
    self.assertEqual(result, expectation)

  def test_not_found(self):
    arg = {'a': 1}
    _result, err = pluck(arg, 'b')
    self.assertRegexpMatches(str(err) ,r'does not exist')

  def test_nested(self):
    arg = {'a': {'a1': 1}}
    result, _err = pluck(arg, 'a.a1')
    self.assertEqual(result, 1)
    arg = {'a': {'a1': {'a2': 2}}}
    result, _err = pluck(arg, 'a.a1.a2')
    self.assertEqual(result, 2)

  def test_fallback(self):
    arg = {'a': {'a1': 1}}
    fallback = 'FALLBACK'
    result, _err = pluck(arg, 'a.a2', fallback)
    self.assertEqual(result, fallback)
