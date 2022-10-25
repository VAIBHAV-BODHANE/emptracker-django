
import email
import imghdr
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.base import ContentFile

from rest_framework import filters, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters

from EmpDetails.models import Employees, EmployeeLeave
from .serializers import EmployeeRegisterSerializer, LoginSerializer, EmployeeSerializer, EmployeeLeaveSerializer
from .permissions import IsOwnerOrAdmin, EmpOrAdmin

import json, time, base64, io
# from datetime import datetime
# from PIL import Image


# def decodeDesignImage(data):
#     try:
#         data = base64.b64decode(data.encode('UTF-8'))
#         buf = io.BytesIO(data)
#         img = Image.open(buf)
#         return img
#     except:
#         return None


class RegisterEmployeeView(APIView):
    permission_classes = ([AllowAny])

    def post(self, request):
        re_data = json.loads(request.body)
        serializer = EmployeeRegisterSerializer(data=re_data)
        data = {}
        if serializer.is_valid():
            user = serializer.save(re_data)
            data['response'] = "successfully register a new user."
            data['email'] = user.email
            token = Token.objects.get(user=user).key
            data['token'] = token
            my_group, created = Group.objects.get_or_create(name='Employee')
            my_group.user_set.add(user)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = ([AllowAny])

    def post(self, request, *args, **kwargs):
        re_data = json.loads(request.body)
        serializer = LoginSerializer(data=re_data)

        user = authenticate(request, username = request.data['email'], password = request.data['password'])

        if user:
            login(request, user)
            token = Token.objects.filter(user=user).first()
            if token:
                token.delete()
            token = Token.objects.create(user=user)
            user_token = token.key
            g = list(request.user.groups.all().values_list('name', flat=True))
            data = {
                'email': request.data['email'],
                'auth_token': user_token,
                'role': json.dumps(g)
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'message': 'Username or Password Incorrect!'}, status=status.HTTP_404_NOT_FOUND)


class EmployeeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ([IsOwnerOrAdmin])
    serializer_class = EmployeeSerializer
    queryset =  Employees.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name', 'email', 'designation', 'jod')

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            return Employees.objects.all()
        else:
            return Employees.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        return Employees.objects.create_user(Kwargs=serializer.data)

    
class EmployeeLeaves(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ([EmpOrAdmin])
    serializer_class = EmployeeLeaveSerializer
    queryset = EmployeeLeave.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', 'leave_type', 'start_date', 'end_date', 'reason', 'is_approve')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return EmployeeLeave.objects.all()
        else:
            return EmployeeLeave.objects.filter(user=self.request.user)
        
    # def perform_create(self, serializer):
    #     image_bs = self.request.data.get('base_code', None)
    #     print('hhere')
    #     if image_bs:
    #         image_name = self.request.data.get('image_name', int(time.mktime(datetime.now().timetuple())))
    #         imgStr = image_bs.split(';base64')
    #         print(imgStr)
    #         data = ContentFile(base64.b64decode(imgStr[0].encode('UTF-8')), name=image_name)
    #         serializer.attachment=data
    #     return serializer.save(user=self.request.user)