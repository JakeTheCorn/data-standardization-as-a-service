import unittest
from pluck import pluck

# Todo:
#   Errors on invalid doc (no in key, no out key, non-dict types)
#   Parse Nested Structure
#   Design for less mocking 
#   Check for Pluck errors

def engine(doc, data):
    _in = doc.get('in')
    _out = doc.get('out')
    collector = {}
    for out_key in _out:
        in_key = _out.get(out_key)
        data_path = _in.get(in_key)
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


if __name__ == '__main__':
    unittest.main()



