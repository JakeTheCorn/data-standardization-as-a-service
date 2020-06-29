from pluck import pluck
from dict_has_path import dict_has_path

# todo:
#   tons of repetition... is it okay?
#   some code paths might not be investigated
#   more tests
#   this is ugly af

"""
What if this generated an intermediary before having data passed in?
  compile(map, transform) -> d
  maybe do this after integrating current functionality with other pieces
"""

def engine(doc, data):
  if 'out' not in doc or 'in' not in doc:
      return None, 'Doc should contain "in" and "out" keys'
  in_doc = doc.get('in')
  out_doc = doc.get('out')
  if not isinstance(in_doc, dict):
      return None, 'Doc "in" should be of type dict'
  if not isinstance(out_doc, dict):
      return None, 'Doc "out" should be of type dict'
  collector = {}
  for out_key in out_doc:
    out_val = out_doc[out_key]
    if isinstance(out_val, dict):
      collector[out_key] = {}
      for sub_key in out_val:
        if isinstance(out_val[sub_key], dict):
          collector[out_key] = {}
          collector[out_key][sub_key] = engine({
              'in': in_doc,
              'out': out_val[sub_key]
          }, data)
          continue

        path = out_key + '.' + sub_key
        _in_key = out_val[sub_key]
        data_path = in_doc.get(_in_key)
        val, err = pluck(data, data_path)
        if err:
          return None, 'Path not found in data'
        collector[out_key][sub_key] = val
    if isinstance(out_val, str):
      in_doc_has_path, err = dict_has_path(in_doc, out_val)
      if not in_doc_has_path:
        return None, 'Path not found: in:%s' % out_val

      data_path = in_doc.get(out_val)
      val, err = pluck(data, data_path)

      if err:
        return None, 'Path not found in data: %s' % data_path
      collector[out_key] = val

  return collector
