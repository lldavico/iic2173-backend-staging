from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from gruponce.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print("Extracting User Info")
        user_inst = User.objects.get(username=user)
        token['first_name'] = user_inst.first_name
        token['last_name'] = user_inst.last_name
        token['email'] = user_inst.email
        token['username'] = user_inst.username
        token['status'] = user_inst.is_superuser
        print(token)

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
