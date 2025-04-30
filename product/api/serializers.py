from rest_framework import serializers
from django.contrib.auth.models import User
from product import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class AllordersSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = models.OrderPlaced
        exclude = ['user', "id"]
        
    def get_username(self, object):
        # user = User.objects.get(id=object.user)
        user = object.user
        if user is None:
            return None
        else:
            return user.username
        # print(type(user))
        # return object.user
 