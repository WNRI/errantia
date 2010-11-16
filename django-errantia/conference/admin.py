# -*- encoding: UTF-8 -*-
from django.contrib import admin

from conference.models import *

admin.site.register(Conference)
admin.site.register(Talk)
