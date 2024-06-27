from rest_framework import serializers
from bwm.models import *


class BulkUploadSerializer(serializers.ModelSerializer):
    template = serializers.PrimaryKeyRelatedField(queryset=Templates.objects.all())
    file = serializers.FileField(allow_null=True, required=False)
    message = serializers.CharField()
    csv = serializers.FileField(allow_null=True, required=False)
 
    def validate(self, data):
        template = data.get('template')
        file = data.get('file')
        
        if template:
            if template.value == 'plain_message' and file:
                raise serializers.ValidationError("Plain messages should not have a file.")
            if template.value == 'with_image' and not file:
                raise serializers.ValidationError("With Image template requires an image.")
            if template.value == 'with_document' and not file:
                raise serializers.ValidationError("With Document template requires a document.")
            if template.value == 'video_message' and not file:
                raise serializers.ValidationError("Video Message template requires a video.")
        
        return data

    class Meta:
        model = BulkMessages
        fields = ['template', 'file', 'message', 'csv']
        extra_kwargs = {
            'required': False  
        }
        
class TemplatesSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    name=serializers.CharField()
    value = serializers.CharField()
    class Meta:
        model = Templates
        fields = ['id', 'name', 'value']

class GetSentMessagesSerializer(serializers.ModelSerializer):
    phoneNumber = serializers.CharField(source='phone_number')
    batch = serializers.CharField(source='batch_id')
    message = serializers.SerializerMethodField()
    response = serializers.SerializerMethodField()
    status = serializers.CharField()
    created_at= serializers.DateTimeField()
    class Meta:
        model = MessageResponse
        fields = ('phoneNumber', 'batch', 'message', 'response', 'status', 'created_at')

    def get_message(self, obj):
        return obj.batch.message

    def get_response(self, obj):
        response_data = obj.response
        if isinstance(response_data, str):
            return response_data
        elif isinstance(response_data, dict):
            if 'error' in response_data:
                return response_data['error']['message']
            elif 'messages' in response_data:
                return 'Message sent successfully'
            else:
                return 'Unknown'
        else:
            return 'Unknown'

   


