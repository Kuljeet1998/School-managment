from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ClassroomConfig(AppConfig):
    name = 'classroom'

    # def ready(self):
    #     import classroom.signals