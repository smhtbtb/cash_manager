from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout
from .serializers import UserSerializer


class CustomerRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerLogin(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CustomerLogout(APIView):
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     request.auth.delete()
    #     return Response({"message": "You have been logged out."}, status=status.HTTP_200_OK)
    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
