from rest_framework import serializers
from django.contrib.auth.models import User

class UserChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("New password must be at least 8 characters long.")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password'))
        instance.save()
        return instance