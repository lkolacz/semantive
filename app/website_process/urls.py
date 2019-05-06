from django.conf.urls import url

from .views import (
    WebsiteList,
    WebsiteRetrieveAPIView,
)

app_name = 'website_process'
urlpatterns = [
    url('^$', WebsiteList.as_view(), name="list"),
    url('(?P<pk>[0-9]+)/$', WebsiteRetrieveAPIView.as_view(), name="item"),
]
