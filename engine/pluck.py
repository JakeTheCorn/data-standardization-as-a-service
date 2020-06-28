def pluck(obj, path, fallback = None):
  """ pluck({'name': {'first': 'bo'}}, 'name.first') -> 'bo', None"""
  d = dict(obj)
  if '.' not in path:
    if path not in d:
      return fallback, '%s does not exist in %s' % (path, d)
    return d[path], None
  paths = path.split('.')
  first, rest = paths[0], paths[1:]
  if first not in d:
    return fallback, '%s does not exist in %s' % (first, d)
  val = d[first]
  if not isinstance(val, dict):
    return val, 'should be dict'
  return pluck(val, '.'.join(rest), fallback)
