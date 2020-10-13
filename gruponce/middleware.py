def AwsEC2Middleware(get_response):

    def middleware(request):
        response = get_response(request)
        response['EC2-Instance-IP'] = request.META.get('REMOTE_ADDR')
        response['X-Forwarder-For'] = request.META.get('HTTP_X_FORWARDED_FOR')
        return response

    return middleware