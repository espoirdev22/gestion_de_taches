# import logging
# from rest_framework import viewsets, generics, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.contrib.auth import get_user_model, authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import UserSerializer, UserRegistrationSerializer

# # Configuration du logger
# logger = logging.getLogger(__name__)

# # Récupération du modèle utilisateur
# UserModel = get_user_model()

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = UserModel.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = []  # Suppression des permissions

# class UserRegistrationView(generics.CreateAPIView):
#     queryset = UserModel.objects.all()
#     permission_classes = []  # Suppression des permissions
#     serializer_class = UserRegistrationSerializer

#     def get_queryset(self):
#         return UserModel.objects.all()

# class UserDetailView(generics.RetrieveUpdateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = []  # Suppression des permissions

#     def get_object(self):
#         return self.request.user

# class UserLoginView(APIView):
#     permission_classes = []  # Suppression des permissions

#     def post(self, request):
#         try:
#             # Log des données reçues
#             logger.info(f"Login attempt - Données reçues: {request.data}")

#             username = request.data.get("username")
#             password = request.data.get("password")

#             if not username or not password:
#                 return Response(
#                     {"error": "Nom d'utilisateur et mot de passe sont requis"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             user = authenticate(username=username, password=password)

#             if user is not None:
#                 logger.info(f"Utilisateur authentifié: {user.username}")

#                 refresh = RefreshToken.for_user(user)
#                 user_serializer = UserSerializer(user)

#                 return Response({
#                     "message": "Connexion réussie",
#                     "tokens": {
#                         "refresh": str(refresh),
#                         "access": str(refresh.access_token)
#                     },
#                     "user": user_serializer.data
#                 }, status=status.HTTP_200_OK)

#             logger.warning("Échec de l'authentification")
#             return Response(
#                 {"error": "Identifiants incorrects"},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )

#         except Exception as e:
#             logger.error(f"Erreur lors de l'authentification: {str(e)}")
#             return Response(
#                 {"error": "Une erreur interne est survenue"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

import logging
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, UserRegistrationSerializer

# Configuration du logger
logger = logging.getLogger(__name__)

# Récupération du modèle utilisateur
UserModel = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = []  # À restreindre si nécessaire

class UserRegistrationView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # L'utilisateur doit être connecté

    def get_object(self):
        return self.request.user

class UserLoginView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            if not username or not password:
                return Response(
                    {"error": "Nom d'utilisateur et mot de passe requis"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = authenticate(request, username=username, password=password)

            if user:
                logger.info(f"Connexion réussie pour: {username}")

                refresh = RefreshToken.for_user(user)
                user_serializer = UserSerializer(user)

                return Response({
                    "message": "Connexion réussie",
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token)
                    },
                    "user": user_serializer.data
                }, status=status.HTTP_200_OK)

            logger.warning(f"Échec de l'authentification pour: {username}")
            return Response(
                {"error": "Identifiants incorrects"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        except Exception as e:
            logger.error(f"Erreur lors de l'authentification: {str(e)}")
            return Response(
                {"error": "Une erreur interne est survenue"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
