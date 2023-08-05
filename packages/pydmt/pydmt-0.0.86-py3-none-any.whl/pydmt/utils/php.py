def to_php(x):
    if isinstance(x, str):
        return '\'{0}\''.format(x)
    if isinstance(x, bool):
        if x:
            return 'TRUE'
        return 'FALSE'
    if x is None:
        return 'null'
    raise ValueError('dont know how to translate type', type(x), x)
