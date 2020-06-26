import unittest

FALLBACK_FLAG = '_______FALLBACK_FLAG'

def pluck(obj, path, fallback = None):
  """ pluck({'name': {'first': 'bo'}}, 'name.first') -> 'bo'"""
  d = dict(obj)
  if '.' not in path:
    val = d.get(path, FALLBACK_FLAG)
    if val == FALLBACK_FLAG:
      return fallback, Exception(path + ' does not exist in {}'.format(d))
    return val, None
  paths = path.split('.')
  first, rest = paths[0], paths[1:]
  val = d.get(first, FALLBACK_FLAG)
  if val == FALLBACK_FLAG:
    return fallback, Exception(first + ' does not exist in {}'.format(d))
  if not isinstance(val, dict):
    return val, Exception('should be dict')
  return from_obj_path(val, '.'.join(rest), fallback)

class TestPluck(unittest.TestCase):
  def test_simple(self):
    arg = {'a': 1}
    result, _err = pluck(arg, 'a')
    expectation = 1
    self.assertEqual(result, expectation)

  def test_not_found(self):
    arg = {'a': 1}
    _result, err = pluck(arg, 'b')
    self.assertRegex(str(err) ,r'does not exist')

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
