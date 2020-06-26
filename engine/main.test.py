import unittest
from pluck import pluck

# Todo:
#   Errors on invalid doc (no in key, no out key, non-dict types)
#   Parse flat to nested
#   Design for less mocking 
#   Check for Pluck errors

def engine(doc, data, col={}):
    _in = doc.get('in')
    _out = doc.get('out')
    collector = {}
    collector.update(col)
    for out_key in _out:
        out_val = _out.get(out_key)
        if isinstance(out_val, dict):
            d = {
                'in': _in,
                'out': out_val
            }
            collector[out_key] = {}
            for sub_key in out_val:
                if isinstance(out_val[sub_key], dict):
                    collector[sub_key] = engine(d, data, collector)
                else:
                    path = out_key + '.' + sub_key
                    _in_key = out_val[sub_key]
                    _data_path = _in.get(_in_key)
                    val, _err = pluck(data, _data_path)
                    collector[out_key][sub_key] = val

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
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()



