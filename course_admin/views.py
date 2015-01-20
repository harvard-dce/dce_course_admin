from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.core.urlresolvers import reverse
from django.conf import settings
from ims_lti_py.tool_config import ToolConfig
from canvas_api_token.decorators import api_token_required
from canvas import CanvasApi, CourseUpdateError

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
    canvas = CanvasApi.from_request(request)
    selected_term = request.GET.get('term', settings.CURRENT_TERM_ID)
    context = {
        'terms': settings.ENROLLMENT_TERMS,
        'selected_term': selected_term
    }
    return render(request, 'course_admin/course_list.html', context)

@login_required
@api_token_required()
@require_GET
def course_data(request):

    canvas = CanvasApi.from_request(request)
    selected_term = request.GET.get('term', settings.CURRENT_TERM_ID)
    if selected_term == 'all':
        selected_term = None

    try:
        course_data = canvas.get_account_courses(term_id=selected_term)
    except:
        raise
    for course in course_data:
        # is_public set to None when False; force boolean
        course['DT_RowId'] = "course-%s" % course['id']
        course['is_public'] = course.get('is_public') or False
        course['homepage_url'] = "%s/courses/%s" \
            % (canvas.canvas_base_url, course['id'])
        course['syllabus_url'] = "%s/courses/%s/assignments/syllabus" \
            % (canvas.canvas_base_url, course['id'])
    return JsonResponse({ 'data': course_data })

@login_required
@api_token_required()
@require_http_methods(['PUT'])
def update_course(request):
    update = QueryDict(request.body)
    try:
        setting_name = update['name']
        setting_state = update['state'] == 'true'
        course_id = update['course_id']
    except KeyError, e:
        log.error("Invalid update params: %s", str(update))
        return JsonResponse(
            {'error': 'Invalid update params'},
            status=400,
            reason='Invalid update params'
        )

    canvas = CanvasApi.from_request(request)
    try:
        if setting_name == 'is_public':
            resp = canvas.set_course_is_public(course_id, setting_state)
        elif setting_name == 'is_published':
            resp = canvas.set_course_is_published(course_id, setting_state)
        return JsonResponse({
            'course_id': course_id,
            'setting_name': setting_name,
            'setting_state': setting_state
        })
    except CourseUpdateError, e:
        log.error("Course update failed: %s", e.msg)
        return JsonResponse({'error': 'Course update failed'},
                            status=500, reason='Invalid update params')

