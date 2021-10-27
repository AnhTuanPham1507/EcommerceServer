import json

from django.http import QueryDict

class add_token_middleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path in ['/o/token', '/o/token/']:
            q = QueryDict.copy(request.POST)
            json_body = json.loads(request.body)
            q.__setitem__("client_id","gy5Ed8TMO9cKsd2lJGKSnHddXRnMeojMTMTy55mW" )
            q.__setitem__('client_secret', "OqAxOo8QrPueXrunys2m0MKuJs1D5WjHFKQXbt5mou91NaLHJrYdFrjJD1LAhR8rAZeWA5yfiJo4m6AXLM9VDfmphFP35KnscWtzl0tELY7ARzV64qNVq2MlsNVH65gI")
            q.__setitem__('username', json_body['username'])
            q.__setitem__('password', json_body['password'])
            q.__setitem__('grant_type', json_body['grant_type'])
            request.POST = q

        response = self.get_response(request)

        return response