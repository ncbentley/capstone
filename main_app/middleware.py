from django.middleware.csrf import rotate_token
from pprint import pprint

def CSRFRefresh(get_response):

    def process_response(request):
        rotate_token(request)
        response = get_response(request)
        pprint(response)
        return response

    return process_response