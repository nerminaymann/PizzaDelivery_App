from rest_framework import serializers
from .models import CustomUser
from phonenumber_field.serializerfields import PhoneNumberField

class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=80)
    phone_number = PhoneNumberField(allow_blank=False,allow_null=False)
    password = serializers.CharField(min_length=8,write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone_number']

    def validate(self, data):
        username = CustomUser.objects.filter(username=data['username'])
        if username.exists():
            raise serializers.ValidationError("username already taken")

        email = CustomUser.objects.filter(email=data['email'])
        if email.exists():
            raise serializers.ValidationError("email already taken")

        # password = data['password']
        # if password != data['password']:
        #     raise serializers.ValidationError("passwords don't match")

        password = CustomUser.objects.filter(password=data['password'])

        # if password and password[0].lower() != password[1].lower():
        #     raise serializers.ValidationError("passwords don't match")

        phone_number = CustomUser.objects.filter(phone_number=data['phone_number'])
        if phone_number.exists():
            raise serializers.ValidationError("phone number already taken")

        return super().validate(data)





