
import drest
from canvas_api_token.utils import canvas_uri

API_PATH = '/api/v1/'

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
        access_params = {'access_token': access_token}
        super(CanvasApi, self).__init__(canvas_base_url + API_PATH, extra_url_params=access_params)
        self._init_resources()

    def _init_resources(self):
        self.add_resource('account_courses',
                          path='/accounts/%d/courses' % self.account_id)
        self.add_resource('account_terms',
                          path='/accounts/%d/terms' % self.account_id)

