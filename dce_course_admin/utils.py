from django.core.urlresolvers import reverse

def build_url(request, pattern_name):
    path = reverse(pattern_name)
    return request.build_absolute_uri(path)
