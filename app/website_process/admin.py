from django.contrib import admin
from .models import Website, WebsiteImage, WebsiteText


admin.site.register(Website)
admin.site.register(WebsiteImage)
admin.site.register(WebsiteText)
