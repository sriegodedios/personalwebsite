from django.db import models
from localflavor.us.models import USStateField
from django.utils.translation import ugettext as _
from django.forms import ModelForm


class ContactInformation(models.Model):
    username = models.CharField(_("username"), max_length=100, blank=False, unique=True)
    address_1 = models.CharField(_("address 1"), max_length=128, blank=False)
    address_2 = models.CharField(_("address 2"), max_length=128, blank=True)
    city = models.CharField(_("city"), max_length=64, default="Manhattan", blank=False)
    state = USStateField(_("state"), default="KS", blank=False)
    zip_code = models.CharField(_("zip code"), max_length=5, default="66506", blank=False)

    def __str__(self):
        return self.name






#class user(models.Model):


# Create your models here.
