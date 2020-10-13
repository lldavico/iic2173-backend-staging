def AwsEC2Middleware(get_response):

    def middleware(request):
        response = get_response(request)
        response['EC2-Instance'] = request.get_host() 
        return response

    return middleware