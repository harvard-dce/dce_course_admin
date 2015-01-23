from urllib import urlencode
from urlparse import urlparse
import drest
from drest.exc import dRestRequestError, dRestError
from requests.utils import parse_header_links
from canvas_api_token.utils import canvas_uri
from django.http import QueryDict

import logging
log = logging.getLogger(__name__)

API_PATH = '/api/v1/'
MAX_ITEMS_PER_REQUEST = 100
MAX_CONCURRENT_REQUESTS = 4

class CourseUpdateError(dRestRequestError):
    pass

class CanvasApi(drest.API):

    @classmethod
    def from_request(cls, request):
        for session_req in ('LTI_LAUNCH', 'CANVAS_API_OAUTH_TOKEN'):
            if session_req not in request.session:
                raise RuntimeError("request.session missing %s" % session_req)
        canvas_base_url = canvas_uri(request)
        account_id = int(request.session['LTI_LAUNCH']['custom_canvas_account_id'])
        access_token = request.session['CANVAS_API_OAUTH_TOKEN']
        return cls(canvas_base_url, access_token, account_id)

    def __init__(self, canvas_base_url, access_token, account_id):
        self.account_id = account_id
        self.canvas_base_url = canvas_base_url
        self.access_header = {'Authorization': "Bearer %s" % access_token}
        super(CanvasApi, self).__init__(canvas_base_url + API_PATH,
                                        extra_headers=self.access_header,
                                        timeout=60,
                                        serialize=True,
                                        trailing_slash=False)
        self._init_resources()

    def _init_resources(self):
        self.add_resource('courses', path='/courses')
        self.add_resource('account_courses',
                          path='/accounts/%d/courses' % self.account_id)
        self.add_resource('account_terms',
                          path='/accounts/%d/terms' % self.account_id)

    def get_account_course_count(self, term_id=None):
        """
        does a request to the account courses endpoint using "1" as the
        per_page value. the response will contain a Link header which we can parse
        to get the total course count. Note: HEAD requests work with local
        dev instances of canvas but seem to be blocked by canvas cloud
        :param term_id:
        :return: integer
        """
        params = { 'per_page': 1 }
        if term_id is not None:
            params['enrollment_term_id'] = 'sis_term_id:%s' % term_id
        resp = self.make_request('GET', self.account_courses.path, params=params)
        # parse the pagination urls canvas inserts in the response Link: header
        page_links = parse_header_links(resp.headers['link'])
        # parse the url marked 'last' to get total number of pages, i.e. courses
        last_link = next((x for x in page_links if x['rel'] == 'last'), None)
        url_parts = urlparse(last_link['url'])
        page_params = QueryDict(url_parts.query, encoding='utf-8')
        return int(page_params['page'])

    def get_account_courses(self, term_id=None):
        course_count = self.get_account_course_count(term_id)
        params = { 'per_page': MAX_ITEMS_PER_REQUEST }
        if term_id is not None:
            params['enrollment_term_id'] = 'sis_term_id:%s' % term_id
        if course_count > MAX_ITEMS_PER_REQUEST:
            return self._get_account_courses_multi_reqs(params, course_count)
        else:
            return self.account_courses.get(params=params).data

    def _get_account_courses_multi_reqs(self, params, course_count):
        course_data = []
        params['page'] = 1
        while True:
            resp = self.account_courses.get(params=params)
            course_data.extend(resp.data)
            if (params['page'] * MAX_ITEMS_PER_REQUEST) >= course_count:
                break
            params['page'] += 1
        return course_data

    def set_course_is_public(self, course_id, state):
        state = state and 'true' or 'false'
        params = { 'course': { 'is_public': state }}
        return self.courses.put(course_id, params=params)

    def set_course_is_published(self, course_id, state):
        event_action = state and 'offer' or 'claim'
        params = { 'course': { 'event': event_action }}
        return self.courses.put(course_id, params=params)
