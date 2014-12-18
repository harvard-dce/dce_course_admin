from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from ims_lti_py.tool_config import ToolConfig
from dce_course_admin.utils import build_url
from canvas_api_token.decorators import api_token_required

import logging
log = logging.getLogger(__name__)
django_log = logging.getLogger("django")

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
    launch_url = build_url(request, 'lti_launch')
    lti_tool_config = ToolConfig(
        title=app_config['name'],
        launch_url=launch_url,
        secure_launch_url=launch_url,
        extensions=extensions,
        description = app_config['description']
    )

    return HttpResponse(lti_tool_config.to_xml(), content_type='text/xml')

@login_required
@api_token_required(completed_view='course_list')
@require_POST
@csrf_exempt
def lti_launch(request):
    return redirect(reverse('course_list'))

@login_required
@api_token_required()
@require_GET
def course_list(request):
    context = {'message': 'You made it!'}
    return render(request, 'course_admin/course_list.html', context)
