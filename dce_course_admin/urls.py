from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^course_admin/', include('course_admin.urls')),
    url(r'^canvas_api_token/', include('canvas_api_token.urls')),
    url(r'^admin/', include(admin.site.urls))
)
