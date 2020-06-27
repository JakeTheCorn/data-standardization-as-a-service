from pluck import pluck


def engine(doc, data):
  if 'out' not in doc or 'in' not in doc:
      return None, 'Doc should contain "in" and "out" keys'
  _in = doc.get('in')
  _out = doc.get('out')
  if not isinstance(_in, dict):
      return None, 'Doc "in" should be of type dict'
  if not isinstance(_out, dict):
      return None, 'Doc "out" should be of type dict'
  collector = {}
  for out_key in _out:
    out_val = _out.get(out_key)
    if isinstance(out_val, dict):
      collector[out_key] = {}
      for sub_key in out_val:
        if isinstance(out_val[sub_key], dict):
          collector[out_key] = {}
          collector[out_key][sub_key] = engine({
              'in': _in,
              'out': out_val[sub_key]
          }, data)
          continue

        path = out_key + '.' + sub_key
        _in_key = out_val[sub_key]
        _data_path = _in.get(_in_key)
        val, _err = pluck(data, _data_path)
        collector[out_key][sub_key] = val
    if isinstance(out_val, str):
      # if dict_has_path
      data_path = _in.get(out_val)
      if '.' not in data_path:
        collector[out_key] = data.get(data_path)
        continue

      val, _err = pluck(data, data_path)
      collector[out_key] = val

  return collector
