from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import serializers

from .models import EmployeeLeave, Employees

import time, io, base64
from PIL import Image
from datetime import datetime


def decodeDesignImage(data):
    try:
        data = base64.b64decode(data.encode('UTF-8'))
        buf = io.BytesIO(data)
        img = Image.open(buf)
        return img
    except:
        return None


class EmployeeRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employees
        fields = ('id', 'email', 'first_name', 'last_name', 'description', 'jod', 'designation', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, data):
        min_length=1
        
        # print(data)
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if len(data) < 8:
            raise serializers.ValidationError(('Password must contain at least 8 letters'))
        if not any(char.isdigit() for char in data):
            raise serializers.ValidationError(('Password must contain at least %(min_length)d digit.') % {'min_length': min_length})
        if not any(char.isalpha() for char in data):
            raise serializers.ValidationError(('Password must contain at least %(min_length)d letter.') % {'min_length': min_length})
        if not any(char in special_characters for char in data):
            raise serializers.ValidationError(('Password must contain at least %(min_length)d special character.') % {'min_length': min_length})
        return data

    def save(self, data):
        if not ('jod' in data.keys()):
            data = Employees.objects.create_user(
                email=self.validated_data['email'],
                first_name=self.validated_data['first_name'],
                last_name=self.validated_data['last_name'],
                designation=self.validated_data['designation'],
                jod=None
            )
        else:
            data = Employees.objects.create_user(
                email=self.validated_data['email'],
                first_name=self.validated_data['first_name'],
                last_name=self.validated_data['last_name'],
                designation=self.validated_data['designation'],
                jod=self.validated_data['jod']
            )
        password=self.validated_data['password']
        data.set_password(password)
        data.save()
        return data


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, required=True
    )

    class Meta:
        model = Employees
        fields = (
            'email',
            'password'
        )


class EmployeeSerializer(serializers.ModelSerializer):
    
    # first_name = serializers.CharField(required=False)
    # last_name = serializers.CharField(required=False)
    # description = serializers.CharField(required=False)
    # designation = serializers.CharField(required=False)
    # password = serializers.CharField(
    #     style={'input_type': 'password'}, write_only=True, required=True
    # )

    class Meta:
        model = Employees
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'description',
            'designation',
            "jod"
        )


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    

    
class EmployeeLeaveSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeLeave
        fields = ('id', 'user', 'leave_type', 'start_date', 'end_date', 'reason', 'attachment', 'is_approve', 'created', 'modified', 'full_name')

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def create(self, validated_data):
        request = self.context['request']
        image_bs = request.data.get('base_code', None)
        image_bs = image_bs.split(';base64')[1]
        curr_time = time.mktime(datetime.now().timetuple())
        if image_bs:
            image_name = request.data.get('image_name', str(int(curr_time)))
            img = decodeDesignImage(image_bs)
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG')
            f_img = InMemoryUploadedFile(img_io, field_name=None, name=image_name, content_type='image/jpeg', size=img_io.tell, charset=None)
            emp = EmployeeLeave.objects.create(
                start_date=validated_data.get('start_date'),
                end_date=validated_data.get('end_date'),
                reason=validated_data.get('reason'),
                attachment=f_img,
                user=request.user,
            )
            if request.data.get('leave_type'):
                emp.leave_type = request.data.get('leave_type')
                emp.save()
            return emp
        return []

    