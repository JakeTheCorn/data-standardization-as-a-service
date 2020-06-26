import unittest


# Todo:
#   Look in the doc for path and output the data in the path
#   Design for less mocking

def engine(doc, data):
    _in = doc.get('in')
    _out = doc.get('out')
    collector = {}
    for out_key in _out:
        in_key = _out.get(out_key)
        data_path = _in.get(in_key)
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


if __name__ == '__main__':
    unittest.main()



