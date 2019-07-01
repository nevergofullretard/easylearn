from django.contrib import admin
from .models import Confirm_email, Password_reset

admin.site.register(Confirm_email)
admin.site.register(Password_reset)
