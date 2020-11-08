from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from backend.settings import env
import requests



class AuthorizationView(APIView):
    permission_classes = [AllowAny]

    # def get(self, request, format=None):
    #     client_secret = "pJhRgb5eEOXqbZPt3qCptIlr6Wab1jA5v995eCoC2prZWWFNpw3f9Wtzt3K3Gh7WezliP2mVqboMRbnE0Y0S07dP5MVX7XihEgCBn0PwIzN6KNDSfNZPTyc49TnILffv"
    #     client_id = "aLJ5YOany5VjU3Jcn5UAfCdtCku5FHTqrWXKVRAA"
    #     response_dict = {"secret": client_secret, "id": client_id}
    #     return Response(response_dict)



    def get(self, request):

        print(request)
        client_secret = env("client_secret")
        client_id = env("client_id")
        callback_uri = env("callback_uri")
        user_token = request.GET["code"]
        token_url = env("token_url")

        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': user_token,
        'redirect_uri': callback_uri,
        'grant_type': 'authorization_code'
        }

        response_auth = requests.post(token_url, headers=headers, data=data)
        print(response_auth.json())
        return Response(response_auth.json())
