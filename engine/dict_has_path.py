def dict_has_path(d, path):
  if not isinstance(d, dict):
    return None, 'dict_has_path expected type dict for d parameter. called with %s' % d.__class__.__name__
  if not isinstance(path, str):
    return None, 'dict_has_path expected type str for path parameter.  called with %s' % path.__class__.__name__
# attempt simple match
  if path in d:
    return True, None
  if '.' not in path:
    return False, None
  sub_paths = path.split('.')
  first, rest = sub_paths[0], sub_paths[1:]
  if first not in path:
    return False, None
  next_val = d.get(first)
  if not isinstance(next_val, dict):
    return False, None
  return dict_has_path(next_val, '.'.join(rest))
