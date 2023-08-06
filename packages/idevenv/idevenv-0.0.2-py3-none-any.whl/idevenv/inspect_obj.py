# -*- coding: utf-8 -*-
import re

from idevenv.viewer import *

def _inspect_obj(o, target='method', linelen=90, linesimbol='-'):
    print(f"type(o): {type(o)}")

    line = linesimbol * linelen

    print('형식: callable(elem) | type(elem) --> rv | type(rv)')

    for e in dir(o):
        a = getattr(o, e)
        if callable(a):
            try:
                a()
            except Exception as err:
                # v = f"!!!Exception!!! {err}"
                if target == 'method_param':
                    print(line, e)
                    print(callable(a), type(a), '-->', err)
            else:
                if target == 'method':
                    v = a()
                    print(line, e)
                    print(callable(a), type(a), '-->', v, type(v))
        else:
            if target == 'gv':
                print(line, e)
                print(callable(a), type(a), '-->', a)


class ObjectInspector(object):
    def __init__(self, target='method', linelen=90, linesimbol='-'):
        d = locals()
        del d['self']
        for k,v in d.items():
            setattr(self, k, v)

    def view(self, obj):
        _inspect_obj(obj)


def inspect_mod(m, title=None, target='gv'):
    s = repr(m) if title is None else title
    pretty_title(s)
    _inspect_obj(m, target)


def inspect_cls(cls, title=None, target='method'):
    s = repr(cls) if title is None else title
    pretty_title(s)
    _inspect_obj(cls, target)
