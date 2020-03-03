import threading

from .app import RoldenSprintApp


def component_init(**kwargs):
    # this component init is blocking and should be run in main thread
    # for some reason it doesn't like to run in thread

    instance = RoldenSprintApp()
    instance.run()

