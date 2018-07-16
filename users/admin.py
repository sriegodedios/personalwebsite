from django.contrib import admin
from users.models import ContactInformation, Profile, Pin
admin.site.register(ContactInformation)
admin.site.register(Profile)
admin.site.register(Pin)

# Register your models here.
