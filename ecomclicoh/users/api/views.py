from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from rest_framework_simplejwt.tokens import AccessToken


class UserLogin(APIView):
    def post(self, request):

        email = request.data["email"]
        password = request.data["password"]
        user = User.objects.filter(email=email).first()
        if user is None:

            raise AuthenticationFailed("Usuario o Contraseña invalidos")
        if not user.check_password(password):

            raise AuthenticationFailed("Usuario o Contraseña invalidos")

        # Capturo el token para el usuario
        usertoken = str(AccessToken.for_user(user))

        print(usertoken)
        return Response(
            {"message": "Logueado Correctamente", "jwt": usertoken, "user_id": user.id},
            status=status.HTTP_200_OK,
        )