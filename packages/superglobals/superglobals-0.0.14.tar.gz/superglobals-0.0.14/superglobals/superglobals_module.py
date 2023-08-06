import inspect

def superglobals():
    """
    returns what `globals()` would return from __main__ context
    """
    _globals = dict(inspect.getmembers(
                inspect.stack()[len(inspect.stack()) - 1][0]))["f_globals"]
    return _globals

def _dotted(key):
    key = key.replace(r'\.', 'PSIOUFJRHPRIUENG')
    pieces = key.split('.')
    return [x.replace('PSIOUFJRHPRIUENG', '.') for x in pieces]

def _ensure_path(_dict, path, create_path):
    for piece in path:
        try:
            if piece in _dict:
                _dict = _dict[piece]
            elif create_path:
                _dict[piece] = dict()
            else:
                return None

        except TypeError:
            if hasattr(_dict, piece):
                _dict = getattr(_dict, piece)
            elif create_path:
                setattr(_dict, piece, dict())
            else:
                return None

        #        if piece not in _dict or not isinstance(_dict[piece], dict):
        #            if not create_path:
        #                return None
        #            _dict[piece] = dict()
        #        _dict = _dict[piece]
    return _dict


def _base(key, create_path):
    _globals = superglobals()

    if isinstance(key, list):
        path = key
    else:
        path = _dotted(key)

    if len(path) == 1:
        return _globals

    base = _ensure_path(_globals, path[0:-1], create_path=create_path)
    return base

def hasglobal(key):
    """
    hasglobal(name) -> bool

    Return whether the global variable `key` exists
    """
    path = _dotted(key)
    base = _base(path, create_path=False)
    if base is not None:
        return path[-1] in base

def getglobal(key, default=None, _type=None):
    """
    getglobal(key[, default]) -> value
    
    Return the value for key if key is in the global dictionary, else default.
    """
    path = _dotted(key)
    base = _base(path, create_path=False)
    piece = path[-1]

    try:
        if piece in base:
            return base[piece]

    except TypeError:
        if hasattr(base, piece):
            return getattr(base, piece)

    return default

def setglobal(key, value):
    """Set `key` from global dictionary

    :param key (str): key
    :param value (any): value
    :raise TypeError: if a heirachical dotted key string's path was invalid
    """
    path = _dotted(key)
    base = _base(path, create_path=True)
    if not isinstance(base, dict):
        raise TypeError("globals::{} was not a dict".format('.'.join(key[0:-1])))
    base[path[-1]] = value

def removeglobal(key, quiet=False):
    """Remove `key` from global dictionary

    :param key (str): key
    :param quiet (bool): fail silently
    :return: True if the key existed
    :raise TypeError: if a heirachical dotted key string's path did not exist
    """
    path = _dotted(key)
    base = _base(path, create_path=False)
    if not isinstance(base, dict):
        if quiet:
            return False
        raise TypeError("globals::{} was not a dict".format('.'.join(key[0:-1])))
    if path[-1] in base:
        base.pop(path[-1])
        return True
    return False

def defaultglobal(key, value):
    """
    defaultglobal(key, value)

    Set the value of global variable `key` if it is not otherwise set and
    return the new/existing contents of the global variable
    """
    path = _dotted(key)
    base = _base(path, create_path=True)
    if not isinstance(base, dict):
        raise TypeError("globals::{} was not a dict".format('.'.join(key[0:-1])))
    if path[-1] not in base:
        base[path[-1]] = value
        return base[path[-1]]
    return base.get(path[-1])
