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
    self.assertRegexpMatches(err ,r'does not exist')
    arg = {'a': {'a1': {'a2': 2}}}
    _result, err = pluck(arg, 'a.a1.a')
    self.assertRegexpMatches(err ,r'does not exist')

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

  def test_unpluckable(self):
    _, err = pluck(1, 'a')
    self.assertRegexpMatches(err, r'unpluckable')
    _, err = pluck({'a': 1}, 'a.b')
    self.assertRegexpMatches(err, r'unpluckable')

  def test_path_not_string(self):
    _, err = pluck({}, None)
    self.assertRegexpMatches(err, r'path must be of type string')

if __name__ == "__main__":
  unittest.main()
