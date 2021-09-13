from django.contrib.auth.models import User
from rest_framework import views
from rest_framework.response import Response
from helpers.jwt_token import encode_token, decode_token


class TokenAuthorize(views.APIView):
    def post(self, request):
        input_token = request.data.get('token')

        if input_token is None:
            return Response({"message": "Token wasn`t provided"}, status=400)
        if input_token == "":
            return Response({'message': "Empty token not allowed"}, status=400)

        jwt_data = decode_token(input_token)
        username = jwt_data.get("username")
        password = jwt_data.get("password")

        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response({'message': 'Invalid token data'}, status=400)

        jwt_response = encode_token({
            "is_admin": user.is_superuser,
            "is_moderator": False,
        })

        return Response({"jwt": jwt_response}, status=200)


class GetToken(views.APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            return Response({"message": "Invalid username or password"}, status=400)

        jwt_token = encode_token({
            "username": username,
            "password": password,
        })

        return Response({'jwt': jwt_token, "message": "Your personal access token, keep it in secret!"}, status=200)


class GetUser(views.APIView):
    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({'message': 'User not found'}, status=404)

        return Response({"id": user.pk,
                         "fullname": "{} {}".format(user.first_name, user.last_name),
                         "admin": user.groups.filter(name='moderator').exists() or user.is_superuser}, status=200)
