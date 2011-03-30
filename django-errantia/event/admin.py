# -*- encoding: UTF-8 -*-
from django.contrib import admin

from event.models import *

class EventAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Event, EventAdmin)
