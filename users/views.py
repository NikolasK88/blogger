from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from users.serializers import UserSerializer, AuthTokenSerializer, BloggerSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from core import models
from datetime import datetime
from core.management.create_blogger import create_or_update_blogger


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateBloggerView(APIView):
    """Create a new blogger in the system"""
    serializer_class = UserSerializer

    def post(self, request):
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        sex = request.data.get('sex', None)
        date_of_birth = request.data.get('date_of_birth', None)
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)
        password1 = request.data.get('password1', None)
        password2 = request.data.get('password2', None)
        languge_id = request.data.get('languge', None)
        country_city_id = request.data.get('country_city', None)
        specialization_id = request.data.get('specialization', None)
        is_conditions_accepted = request.data.get('is_conditions_accepted', False)

        if is_conditions_accepted:
            is_conditions_accepted = True

        if password1 != password2:
            return Response({'error': 'Passwords missmatch'}, status=status.HTTP_400_BAD_REQUEST)

        if date_of_birth:
            date_of_birth = datetime.strptime(date_of_birth, "%d-%m-%Y")#22-05-2021

        serializer = self.serializer_class(data={'email': email,
                                                 'phone': phone,
                                                 'user_role': 'blogger',
                                                 'password': password1}
                                           )
        if serializer.is_valid():
            serializer.save()
            try:
                user = get_user_model().objects.get(email=email)
            except:
                return Response({'error': 'User wasn\'t created'}, status=status.HTTP_400_BAD_REQUEST)

            blogger_exist = models.BloggerAccount.objects.filter(user=user).exist()
            if blogger_exist:
                return Response({'error': 'You already have a blogger account'}, status=status.HTTP_400_BAD_REQUEST)
            blogger = create_or_update_blogger

            if blogger != True:
                return blogger

            return Response(BloggerSerializer(models.BloggerAccount.objects.get(user=user)).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

#     'first_name', 'last_name', 'sex', 'date_of_birth', 'email', 'phone',
#                   'password1', 'password2', 'languge', 'country_city', 'specialization',
#                   'user_role'

class LoginView(ObtainAuthToken):
    """Obtain a new auth token for user"""
    serializer_class = AuthTokenSerializer
    # renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    renderer_classes = [JSONRenderer]


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrive and return authentication user"""
        return self.request.user


class EditUser(APIView):
    """Edit user info"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, pk=None, *args, **kwargs):
        user_id = self.kwargs['user_id']

        try:
            user = get_user_model().objects.get(id=user_id)
        except:
            return Response({'error': 'No such user'}, status=status.HTTP_400_BAD_REQUEST)



        # user = get_user_model().objects.update_or_create(
        #     id=user_id,
        #     defaults={
        #         'first_name': first_name,
        #         'last_name': last_name,
        #         'sex': sex,
        #         'date_of_birth': date_of_birth,
        #         'email': email,
        #         'phone': phone,
        #         'phone': phone,
        #     }
        # )[0]
        return Response()
