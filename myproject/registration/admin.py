from django.contrib import admin
from .models import UserDetails, BiometricDetails

admin.site.register(UserDetails)
admin.site.register(BiometricDetails)