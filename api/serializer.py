from rest_framework import serializers
from api.models import ToDosn
from  django.contrib.auth.models import User


class TodoSerializer(serializers.ModelSerializer):
    User=serializers.CharField(read_only=True)
    Status=serializers.CharField(read_only=True)
    class Meta:
        model=ToDosn
        fields=["Task_name","User","Status"]

    def create(self,validated_data):
        usr=self.context.get("User")
        return ToDosn.objects.create(**validated_data,User=usr)


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password"]        


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)