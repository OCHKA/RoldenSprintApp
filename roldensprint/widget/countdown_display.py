import datetime

from kivy.properties import NumericProperty
from kivy.uix.label import Label

from roldensprint import util


class CountDownDisplay(Label):
    time = NumericProperty(0)

    def on_time(self, instance, new_time):
        new_datetime = datetime.timedelta(seconds=new_time)
        self.text = str(new_datetime)


# util.load_kv_file()
