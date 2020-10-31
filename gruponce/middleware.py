from django.conf import settings

def AwsEC2Middleware(get_response):

    def middleware(request):
        response = get_response(request)
        response['EC2-Instance-IP'] = settings.AWS_EC2_IP
        response['EC2-Instance-DNS'] = settings.AWS_EC2_DNS
        return response

    return middleware