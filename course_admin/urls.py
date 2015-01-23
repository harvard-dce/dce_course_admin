from django.conf.urls import patterns, url

urlpatterns = patterns('course_admin.views',
    url(r'^tool_config$', 'tool_config'),
    url(r'^lti_launch$', 'lti_launch', name='lti_launch'),
    url(r'^course_admin$', 'course_admin', name='course_admin'),
    url(r'^course_data$', 'course_data', name='course_data'),
    url(r'^update_course$', 'update_course', name='update_course')
)
