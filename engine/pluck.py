def pluck(obj, path, fallback = None):
  """ pluck({'name': {'first': 'bo'}}, 'name.first') -> 'bo', None"""
  if not isinstance(path, str):
    return fallback, 'path must be of type string'
  if not isinstance(obj, dict):
    return fallback, 'unpluckable! pluck expected type dict'
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
  return pluck(val, '.'.join(rest), fallback)
