import json


def get_request_parameters(request):
    """ Return dic of request params """
    parameters = {}
    if request.body:
        # Decode data to a dict object
        json_data = json.loads(request.body.decode('utf-8'))
        parameters = json_data
    return parameters
