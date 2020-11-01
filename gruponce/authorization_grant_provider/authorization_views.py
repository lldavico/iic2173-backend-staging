from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny


class AuthorizationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        client_secret = "pJhRgb5eEOXqbZPt3qCptIlr6Wab1jA5v995eCoC2prZWWFNpw3f9Wtzt3K3Gh7WezliP2mVqboMRbnE0Y0S07dP5MVX7XihEgCBn0PwIzN6KNDSfNZPTyc49TnILffv"
        client_id = "aLJ5YOany5VjU3Jcn5UAfCdtCku5FHTqrWXKVRAA"
        response_dict = {"secret": client_secret, "id": client_id}
        return Response(response_dict)

