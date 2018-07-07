from django.db import models
from localflavor.us.models import USStateField
from django.utils.translation import ugettext as _
from django.forms import ModelForm
from django.contrib.auth.models import User



def userpath(instance, filename):
    return "users/%s/%s" %(instance.user.username, filename)

class ContactInformation(models.Model):
    username = models.CharField(_("username"), max_length=100, blank=False, unique=True)
    address_1 = models.CharField(_("address 1"), max_length=128, blank=False)
    address_2 = models.CharField(_("address 2"), max_length=128, blank=True)
    city = models.CharField(_("city"), max_length=64, default="Manhattan", blank=False)
    state = USStateField(_("state"), default="KS", blank=False)
    zip_code = models.CharField(_("zip code"), max_length=5, default="66506", blank=False)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
                                User,
                                on_delete=models.DO_NOTHING,
                                )
    picture = models.ImageField(upload_to = userpath)
    Address = models.OneToOneField(
                                    ContactInformation,
                                    on_delete=models.DO_NOTHING,

                                    )
    def __str__(self):
        return self.user.username




#class user(models.Model):


# Create your models here.
