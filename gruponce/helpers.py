import json
import re

import boto3
import jwt
from backend.settings import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY
from django.conf import settings

from gruponce.models import User

SECRET_KEY = settings.SECRET_KEY


def get_request_parameters(request):
    """ Return dic of request params """
    parameters = {}
    if request.data:
        # Decode data to a dict object
        json_data = request.data
        parameters = json_data
    return parameters


def get_token_decoded(META):
    """ Return Token of request """
    regex_meta = re.compile('^HTTP_')
    request_meta = dict((regex_meta.sub('', header), value)
                        for (header, value) in META.items() if header.startswith('HTTP_'))
    if 'AUTHORIZATION' not in request_meta:
        return False
    token = request_meta['AUTHORIZATION']
    token_type = token.split(' ')[0]
    token = token.split(' ')[1]
    print("Token: {}".format(token))
    print("Token Type: {}".format(token_type))
    return token


def get_user_from_meta(meta_data):
    """ Return a user associated to the given user """
    token = get_token_decoded(meta_data)
    res_dict = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    if res_dict['user_id'] is None:
        print('Invalid Token')
        return False
    if not User.objects.filter(id=res_dict['user_id']).exists():
        print("User doesnt exists")
        return False
    user = User.objects.get(id=res_dict['user_id'])
    return user



# AWS SENTIMENT


def analyze(text):
    
    comprehend = boto3.client(service_name='comprehend', region_name=AWS_REGION, aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)               
    to_return = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return to_return["Sentiment"]


