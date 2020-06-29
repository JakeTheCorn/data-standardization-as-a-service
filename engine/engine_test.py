import unittest
from engine import Engine

# Todo:
#   Reformat to use 2 spaces
#   Errors on invalid doc
#   Lists?
#   Design for less mocking?
#   Test for Pluck errors (then implement)
#   rename indoc to parse_map?
#   spec mixin behavior

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
      e = Engine(doc)
      actual, err = e.run(data)
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

    e = Engine(doc)
    actual, err = e.run(data)
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

    e = Engine(doc)
    actual, err = e.run(data)
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

      e = Engine(doc)
      actual, err = e.run(data)
      expected = {'user': {'name': {'first': 'bob', 'last': 'bobson'}}}
      self.assertEqual(actual, expected)

  def test_it_errors_when_no_in_or_out_keys_in_doc(self):
      doc = {'in': None}
      e = Engine(doc)
      actual, err = e.run({})
      self.assertEqual('Doc should contain "in" and "out" keys', err)
      doc = {'out': None}
      e = Engine(doc)
      actual, err = e.run({})
      self.assertEqual('Doc should contain "in" and "out" keys', err)

  def test_in_datatype_err(self):
      doc = {'in': None, 'out': {}}
      e = Engine(doc)
      actual, err = e.run({})
      self.assertEqual('Doc "in" should be of type dict', err)

  def test_out_datatype_err(self):
    doc = {'in': {}, 'out': None}
    e = Engine(doc)
    actual, err = e.run({})
    self.assertEqual('Doc "out" should be of type dict', err)

  # todo
  def _test_list_data(self):
    data = {
      'people': [{'name': 'bob'}]
    }
    doc = {'in': {}, 'out': {}}
    e = Engine(doc)
    actual, err = e.run(data)
    expected = {}
    self.assertEqual(expected, actual)

  def test_flat_path_error_out_doc(self):
    data = {}
    in_doc = {'in_name': 'name'}
    tables = [
      ({'Name': 'not_in_name'}, 'Path not found: in:not_in_name'),
      ({'Name': 'not_in_name2'}, 'Path not found: in:not_in_name2')
    ]
    for out_doc, expected in tables:
      doc = {'in': in_doc, 'out': out_doc}
      e = Engine(doc)
      actual, err = e.run(data)
      self.assertEqual(actual, None)
      self.assertEqual(expected, err)

  # test use case of using an in doc like this...
  def test_nested_path_error_out_doc(self):
    data = {}
    in_doc = {'in_name': {'first': 'bo'}}
    out_doc ={'Name': 'in_name.last'}
    doc = {'in': in_doc, 'out': out_doc}
    e = Engine(doc)
    actual, err = e.run(data)
    self.assertEqual(actual, None)
    self.assertEqual(err, 'Path not found: in:in_name.last')

  # maybe? too early?
  def _test_mixin_operation(self):
    data = {
      'location': {
        'address': '11 street ave.'
      },
      'home_details': {
        'has_windows': False
      }
    }
    in_doc = {
      'in_location': 'location',
      'in_home_details': 'home_details'
    }
    out_doc ={'Home': '...in_location, ...in_homedetails'}
    doc = {'in': in_doc, 'out': out_doc}
    e = Engine(doc)
    actual, err = e.run(data)
    expected = {
      'Home': {
        'address': '11 street ave.',
        'has_windows': False
      }
    }
    self.assertEqual(actual, )
    self.assertEqual(err, None)

  def test_path_error_in_doc(self):
    data = {'name': 'bob'}
    doc = {'in': {'in_name': '_'}, 'out': {'Name': 'in_name'}}
    e = Engine(doc)
    actual, err = e.run(data)
    self.assertEqual('Path not found in data: _', err)


if __name__ == '__main__':
  unittest.main()
