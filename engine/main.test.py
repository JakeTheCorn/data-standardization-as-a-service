import unittest
from pluck import pluck

# Todo:
#   Errors on invalid doc (no in key, no out key, non-dict types)
#   Parse flat to nested
#   Design for less mocking 
#   Check for Pluck errors
#   Recurse to get nested from flat

def engine(doc, data):
    _in = doc.get('in')
    _out = doc.get('out')
    collector = {}
    for out_key in _out:
        out_val = _out.get(out_key)
        if isinstance(out_val, dict):
            d = {
                'in': _in,
                'out': out_val
            }
            return engine(d, data)
        if isinstance(out_val, str):
            data_path = _in.get(out_val)
            if '.' in data_path:
                val, _err = pluck(data, data_path)
                collector[out_key] = val
                continue
            collector[out_key] = data.get(data_path)
    
    return collector


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
        expected = {'Name' : 'Frank'}
        self.assertEqual(actual, expected)

    def test_flat_to_nested(self):
        data = {
            'user_first': 'bob',
            'user_last': 'bobson'
        }
        doc = {
            'in': {
                'user_first' : 'user_first',
                'user_last': 'user_last'
            },
            'out' : {
                'user' : {
                    'first': 'user_first',
                    'last': 'user_last'
                }
            }
        }

        actual = engine(doc=doc, data=data)
        expected = {'user': {'first': 'bob', 'last': 'bobson'}}
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()



