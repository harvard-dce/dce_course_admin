from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.core.urlresolvers import reverse
from django.conf import settings
from ims_lti_py.tool_config import ToolConfig
from canvas_api_token.decorators import api_token_required
from canvas import CanvasApi

import logging
log = logging.getLogger(__name__)

@require_GET
def index(request):
    pass

@require_GET
def tool_config(request):

    app_config = settings.LTI_APPS['course_admin']
    nav_settings = {
        'enabled': 'true',
        'text': app_config['menu_title']
    }
    extensions = {
        app_config['extensions_provider']: {
            'account_navigation': nav_settings,
            'tool_id': app_config['id'],
            'privacy_level': app_config['privacy_level']
        }
    }
    launch_url = request.build_absolute_uri(reverse('lti_launch'))
    lti_tool_config = ToolConfig(
        title=app_config['name'],
        launch_url=launch_url,
        secure_launch_url=launch_url,
        extensions=extensions,
        description = app_config['description']
    )

    return HttpResponse(lti_tool_config.to_xml(), content_type='text/xml')

@login_required
@api_token_required(completed_view='course_admin')
@require_POST
@csrf_exempt
def lti_launch(request):
    return redirect(reverse('course_admin'))

@login_required
@api_token_required()
@require_GET
def course_admin(request):
    course_data_url = request.build_absolute_uri(reverse('course_data'))
    context = { 'course_data_url': course_data_url }
    return render(request, 'course_admin/course_list.html', context)

@login_required
@api_token_required()
@require_GET
def course_data(request):

    from random import choice
    canvas = CanvasApi.from_request(request)
    course_data = canvas.account_courses.get(params={ 'per_page': 1000 }).data
    for course in course_data:
        course['homepage_url'] = "%s/courses/%s" % (canvas.canvas_base_url, course['id'])
        course['is_public'] = choice((True, True, True, False)), # TODO:
    return JsonResponse({ 'data': course_data })


