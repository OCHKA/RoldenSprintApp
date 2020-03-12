import importlib
import typing
import logging

__registered_components: typing.Dict[str, typing.List[typing.Dict]] = {}


def add_component(package_name: str, **kwargs) -> None:
    logging.info(f"core.registry: {package_name}")

    module = importlib.import_module(package_name)
    instance = module.component_init(**kwargs)

    if package_name not in __registered_components.keys():
        __registered_components[package_name] = []

    __registered_components[package_name].append(instance)
