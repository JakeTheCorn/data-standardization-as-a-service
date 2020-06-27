import unittest
from engine import engine

# Todo:
#   Reformat to use 2 spaces
#   Errors on invalid doc
#   Lists?
#   Design for less mocking?
#   Test for Pluck errors (then implement)

class EngineTest(unittest.TestCase):
  def test_basic_flat(self):
    tables = [
      ({'name': 'bob'}, {'name': 'name'}, {'Name': 'name'}, {'Name': 'bob'}),
      ({'age': 45}, {'age': 'age'}, {'Age': 'age'}, {'Age': 45}),
      ({'age': 46}, {'hasAge': 'age'}, {'HasAge': 'hasAge'}, {'HasAge': 46})
    ]
    for data, in_doc, out_doc, expected in tables:
      doc = {
          'in': in_doc,
          'out': out_doc
      }
      actual = engine(doc=doc, data=data)
      self.assertEqual(actual, expected)

  def test_nested_to_flat(self):
    data = {
      'user' : {
        'name' : 'Frank'
      }
    }
    doc = {
      'in': {
        'name' : 'user.name'
      },
      'out' : {
        'Name' : 'name'
      }
    }

    actual = engine(doc=doc, data=data)
    expected = {'Name': 'Frank'}
    self.assertEqual(actual, expected)

  def test_flat_to_nested(self):
    data = {
      'user_first': 'bob',
      'user_last': 'bobson'
    }
    doc = {
      'in': {
        'in_first' : 'user_first',
        'in_last': 'user_last'
      },
      'out' : {
        'user' : {
          'first': 'in_first',
          'last': 'in_last'
        }
      }
    }

    actual = engine(doc=doc, data=data)
    expected = {'user': {'first': 'bob', 'last': 'bobson'}}
    self.assertEqual(expected, actual)

  def test_flat_to_deeply_nested(self):
      data = {
          'user_first': 'bob',
          'user_last': 'bobson'
      }
      doc = {
          'in': {
              'in_first' : 'user_first',
              'in_last': 'user_last'
          },
          'out' : {
              'user' : {
                  'name': {
                      'first': 'in_first',
                      'last': 'in_last'
                  }
              }
          }
      }

      actual = engine(doc=doc, data=data)
      expected = {'user': {'name': {'first': 'bob', 'last': 'bobson'}}}
      self.assertEqual(actual, expected)

  def test_it_errors_when_no_in_or_out_keys_in_doc(self):
      doc = {'in': None}
      _res, err = engine(doc, {})
      self.assertEqual('Doc should contain "in" and "out" keys', err)
      doc = {'out': None}
      _res, err = engine(doc, {})
      self.assertEqual('Doc should contain "in" and "out" keys', err)

  def test_in_datatype_err(self):
      doc = {'in': None, 'out': {}}
      _res, err = engine(doc, {})
      self.assertEqual('Doc "in" should be of type dict', err)

  def test_out_datatype_err(self):
    doc = {'in': {}, 'out': None}
    _res, err = engine(doc, {})
    self.assertEqual('Doc "out" should be of type dict', err)

  # todo
  def _test_list_data(self):
    data = []
    doc = {'in': {}, 'out': {}}
    actual, err = engine(doc, data)
    expected = {}
    self.assertEqual(expected, actual)

  def test_path_error_out_doc(self):
    data = {'name': 'bob'}
    doc = {'in': {'in_name': 'name'}, 'out': {'Name': 'not_in_name'}}
    actual, err = engine(doc, data)
    self.assertEqual('Path not found', err)


if __name__ == '__main__':
    unittest.main()
