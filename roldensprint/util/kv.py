import os
import inspect

from kivy.lang import Builder


def load_kv_file():
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])

    path = os.path.dirname(mod.__file__)
    filename = os.path.basename(mod.__file__).replace('.py', '.kv')
    kv_file = os.path.join(path, filename)

    Builder.load_file(kv_file)
