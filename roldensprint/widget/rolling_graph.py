import os

from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.lang import Builder
# from kivy.uix.widget import


class RollingGraph(Widget):
    points = ListProperty([(0, 100), (200, 600)])

    pass


script_dir = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(script_dir + '/rolling_graph.kv')
