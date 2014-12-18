from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^course_admin/', include('course_admin.urls')),
    url(r'^canvas_api_token/', include('canvas_api_token.urls'))
)
