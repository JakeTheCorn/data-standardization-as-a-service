def dict_has_path(v, path):
  if not isinstance(v, dict):
    return None, 'dict_has_path expected type dict for v parameter. called with %s' % v.__class__.__name__
  if not isinstance(path, str):
    return None, 'dict_has_path expected type str for path parameter.  called with %s' % path.__class__.__name__
  if path in v:
    return True, None
  if '.' not in path:
    return False, None
  sub_paths = path.split('.')
  first, rest = sub_paths[0], sub_paths[1:]
  if first not in path:
    return False, None
  next_val = v[first]
  if not isinstance(next_val, dict):
    return False, None
  return dict_has_path(next_val, '.'.join(rest))
