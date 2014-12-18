from django.conf.urls import patterns, url

urlpatterns = patterns('course_admin.views',
    url(r'^$', 'index'),
    url(r'^tool_config$', 'tool_config'),
    url(r'^lti_launch$', 'lti_launch', name='lti_launch'),
    url(r'^course_list$', 'course_list', name='course_list'),
)
