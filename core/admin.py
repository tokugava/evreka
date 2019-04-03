from django.contrib import admin

from .models import Public_Message, Poll_Choice, User_Choice, Private_Message, Site, Site_User, Public_Image, Private_Image

admin.site.register(Public_Message)
admin.site.register(Poll_Choice)
admin.site.register(User_Choice)
admin.site.register(Private_Message)
admin.site.register(Site)
admin.site.register(Site_User)
admin.site.register(Public_Image)
admin.site.register(Private_Image)