from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
from bwm.tasks import *
from rest_framework import status
from bwm.messaging import *
import logging
from django.utils import timezone
from django.db.models import Count
from users.serializers import UserChangePasswordSerializer
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

logger = logging.getLogger(__name__)

class CustomAuthentication:
    def authenticate(self, request):
        username = request.headers.get('apiUsername')
        password = request.headers.get('apiPassword')

        user = authenticate(request, username=username, password=password)
        if user:
            return (user, None)
        else:
            raise AuthenticationFailed('User not authenticated')

    def authenticate_header(self, request):
        return 'Bearer'

class UploadCSV(APIView):
    authentication_classes = [CustomAuthentication]  

    def post(self, request):
        serializer = BulkUploadSerializer(data=request.data)
        if serializer.is_valid():
            bulk_message = serializer.save()
            process_csv_file.delay(bulk_message.id)
            logger.info(f'File Processing for batch {bulk_message}')
            print('processing file')
            return Response({'message': 'File processing started successfully'})
        logger.error(f'An error occurred: {serializer.errors}')
        return Response(serializer.errors, status=400)

    def handle_exception(self, exc):
        if isinstance(exc, AuthenticationFailed):
            logger.error(f'An error occurred while validating user : {exc}')
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return super().handle_exception(exc)

class TemplatesApiView(APIView):
    authentication_classes = [CustomAuthentication]  

    def get(self, request):
        try:
            templates = Templates.objects.all()
            serializer = TemplatesSerializer(templates, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_message = str(e)
            logger.error(f'An error occurred : {error_message}')
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_exception(self, exc):
        if isinstance(exc, AuthenticationFailed):
            logger.error(f'An error occurred while validating user : {exc}')
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return super().handle_exception(exc)


class GetSentMessagesView(APIView):
    authentication_classes = [CustomAuthentication]  

    def get(self, request, format=None):
        try:
            queryset = MessageResponse.objects.filter(created_at__date=timezone.now().date())
            serializer = GetSentMessagesSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            logger.error(f'An error occurred : {error_message}')
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_exception(self, exc):
        if isinstance(exc, AuthenticationFailed):
            logger.error(f'An error occurred while validating user : {exc}')
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return super().handle_exception(exc)

class GetAllSentMessagesView(APIView):
    authentication_classes = [CustomAuthentication]  

    def get(self, request, format=None):
        try:
            queryset = MessageResponse.objects.all()
            serializer = GetSentMessagesSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            logger.error(f'An error occurred : {error_message}')
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_exception(self, exc):
        if isinstance(exc, AuthenticationFailed):
            logger.error(f'An error occurred while validating user : {exc}')
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return super().handle_exception(exc)


class GetMessageStatistics(APIView):
    authentication_classes = [CustomAuthentication]  

    def get(self, request, format=None):
        try:
            today = timezone.now().date()
            queryset = MessageResponse.objects.filter(created_at__date=today).values('status').annotate(count=Count('status'))
            
            status_counts = {
                'failed': 0,
                'successful': 0,
                'total':0
            }
            
            for entry in queryset:
                if entry['status'].lower() == 'failed':
                    status_counts['failed'] = entry['count']
                elif entry['status'].lower() == 'successful':
                    status_counts['successful'] = entry['count']
                status_counts['total'] += entry['count']

            return Response(status_counts, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            logger.error(f'An error occurred: {error_message}')
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_exception(self, exc):
        if isinstance(exc, AuthenticationFailed):
            logger.error(f'An error occurred while validating user: {exc}')
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return super().handle_exception(exc)

class UserChangePasswordView(APIView):
    authentication_classes = [CustomAuthentication] 
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
    password_serializer_class = UserChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.password_serializer_class(data=request.data)
            if serializer.is_valid():
                user_id = serializer.validated_data["user_id"]
                try:
                    user = User.objects.get(id=user_id)
                    if user.check_password(serializer.validated_data["old_password"]):
                        serializer.update(user, serializer.validated_data)
                        return Response({"message": "Password Updated Successfully"}, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            "success": False,
                            "message": "Incorrect Old Password"
                        }, status=status.HTTP_400_BAD_REQUEST)
                except User.DoesNotExist:
                    return Response({
                        "success": False,
                        "message": "User not found"
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    "success": False,
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Exception: {e}")
            return Response({
                "success": False,
                "message": f"An error occurred: {e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)