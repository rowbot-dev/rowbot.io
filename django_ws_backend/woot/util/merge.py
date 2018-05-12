
def merge(*args):
  original, to_merge = args[0], args[1:]

  # merge only the first to_merge
  if to_merge:
    first, rest = to_merge[0], to_merge[1:]

    new = None
    if isinstance(original, dict):
      new = original

      first_is_a_dict = isinstance(first, dict)
      if first_is_a_dict:
        for key, value in first.items():
          if key in original:
            new.update({key: merge(original.get(key), value)})
          else:
            new.update({key: value})
      else:
        new = first

    elif isinstance(original, list):
      new = original

      first_is_a_list = isinstance(first, list)
      if first_is_a_list:
        new.extend(first)
      else:
        new = first

    else:
      new = first

    return merge(new, *rest)

  return original
