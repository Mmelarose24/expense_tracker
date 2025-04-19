from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(Budget)
admin.site.register(Schedule)
admin.site.register(Notification)
# Register your models here.
