from kivy.lang.builder import BuilderBase
from pyexpander.lib import expandToStr


class ExpanderBuilder(BuilderBase):
    def __init__(self, app, builder, definitions: dict):
        super(ExpanderBuilder, self).__init__()
        self.app = app
        self.files = builder.files
        self.dynamic_classes = builder.dynamic_classes
        self.templates = builder.templates
        self.rules = builder.rules
        self.rulectx = builder.rulectx
        self.defs = definitions

    def load_string(self, string, **kwargs):
        xstring = expandToStr(string, external_definitions=self.defs)[0]
        return super(ExpanderBuilder, self).load_string(xstring, **kwargs)
