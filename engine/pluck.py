FALLBACK_FLAG = '_______FALLBACK_FLAG'

def pluck(obj, path, fallback = None):
  """ pluck({'name': {'first': 'bo'}}, 'name.first') -> 'bo'"""
  d = dict(obj)
  if '.' not in path:
    val = d.get(path, FALLBACK_FLAG)
    if val == FALLBACK_FLAG:
      return fallback, Exception(path + ' does not exist in {}'.format(d))
    return val, None
  paths = path.split('.')
  first, rest = paths[0], paths[1:]
  val = d.get(first, FALLBACK_FLAG)
  if val == FALLBACK_FLAG:
    return fallback, Exception(first + ' does not exist in {}'.format(d))
  if not isinstance(val, dict):
    return val, Exception('should be dict')
  return pluck(val, '.'.join(rest), fallback)
