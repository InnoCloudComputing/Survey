from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from Survey import settings

media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
from quest import views

urlpatterns = [
    # url(r'^$', views.index, name='home'),
    url(r'^$', views.survey_detail, name='survey_detail'),
    url(r'^confirm/(?P<uuid>\w+)/$', views.confirm, name='confirmation'),
    # url(r'^privacy/$', views.privacy, name='privacy_statement'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
