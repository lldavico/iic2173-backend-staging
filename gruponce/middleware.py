from django.conf.settings import AWS_EC2_DNS, AWS_EC2_IP 

def AwsEC2Middleware(get_response):

    def middleware(request):
        response = get_response(request)
        response['EC2-Instance-IP'] = AWS_EC2_IP
        response['EC2-Instance-DNS'] = AWS_EC2_DNS
        return response

    return middleware