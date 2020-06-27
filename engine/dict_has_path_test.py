import unittest
from dict_has_path import dict_has_path


class DictHasPathTestsTest(unittest.TestCase):
  def test_called_with_non_dict_error(self):
    has_path, err = dict_has_path(None, 'adsf')
    self.assertEqual(None, has_path)
    self.assertRegexpMatches(err, r'expected type dict')

  def test_called_with_non_string_path(self):
    has_path, err = dict_has_path({}, None)
    self.assertEqual(None, has_path)
    self.assertRegexpMatches(err, r'expected type str')

  def test_shallow_true(self):
    has_path, err = dict_has_path({'age': 1}, 'age')
    self.assertEqual(has_path, True)
    self.assertEqual(err, None)

  def test_shallow_false(self):
    has_path, err = dict_has_path({'age': 1}, 'name')
    self.assertEqual(has_path, False)
    self.assertEqual(err, None)

  def test_nested_true(self):
    has_path, err = dict_has_path({'name': {'first': 'bo'}}, 'name.first')
    self.assertEqual(has_path, True)
    self.assertEqual(err, None)


if __name__ == '__main__':
    unittest.main()
