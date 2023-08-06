# -*- coding: utf-8 -*-
"""Functions utils."""
try:
    from Products.CMFPlone.utils import safe_text
except ImportError:
    # BBB: Plone<5.2 don't have safe_text
    from Products.CMFPlone.utils import safe_unicode as safe_text


def convert_path(path):
    """Convert path to a valid ascii string.
    If it contains non-ascii characters, raises an Exception."""
    try:
        if path.isascii():
            return safe_text(path)
    except AttributeError:
        # BBB: Python 2 and Python 3.6 string doesn't have isascii method.
        try:
            _path = safe_text(path).encode("ascii")
            if not isinstance(_path, str):
                # BBB: Python 3.6: convert byte to string.
                return _path.decode()
            return _path
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
    _path = path
    if not isinstance(_path, str):
        _path = _path.encode("utf-8")
    raise AssertionError(
        'The path "{0}" contains non-ascii characters.'.format(
            _path,
        ),
    )
