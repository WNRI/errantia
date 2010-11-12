# -*- encoding: UTF-8 -*-
"""
@author: Federico Cáceres <fede.caceres@gmail.com>
"""
from django.contrib import admin
from jchat.models import *

admin.site.register(Room)
admin.site.register(Message)
