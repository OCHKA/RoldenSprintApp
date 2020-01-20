#!/usr/bin/env python

import os

from kivy.config import Config

from .app import RoldenSprintApp


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(__file__))
    Config.read(script_dir + '/config.dev.ini')

    RoldenSprintApp().run()
