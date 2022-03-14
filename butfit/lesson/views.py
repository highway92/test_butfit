from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from lesson import serializers,models
from log.models import Lessonlog
from member.models import User
from log.models import Userlog
from drf_yasg             import openapi 
from drf_yasg.utils       import swagger_auto_schema
from django.db.models import Q
# Create your views here.

@permission_classes([IsAuthenticated])
class CheckCreditAPI(APIView):
    user_id = openapi.Parameter('user_id', openapi.IN_PATH, description='user primary key', required=True, type=openapi.TYPE_NUMBER)
    @swagger_auto_schema(manual_parameters=[user_id], responses={200: 'Success'})
    def get(self, request, user_id):
        user = User.objects.get(id = user_id)
        userlog = Userlog.objects.filter(user = user).values()
        return Response({"userlog" : userlog},status = status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
class CheckLessonAPI(APIView):
    user_id = openapi.Parameter('user_id', openapi.IN_PATH, description='user primary key', required=True, type=openapi.TYPE_NUMBER)
    @swagger_auto_schema(manual_parameters=[user_id], responses={200: 'Success'})
    def get(self, request, user_id):
        user = User.objects.get(id = user_id)
        userlog = Userlog.objects.filter(Q(user = user, reason = '구매') |
        Q(user = user, reason = '환불')).values()
        return Response({"userlog" : userlog},status = status.HTTP_200_OK)


@permission_classes([IsAdminUser])
class CreateLessonAPI(APIView):
    @swagger_auto_schema(request_body=serializers.CreateLessonSerializer)
    def post(self, request, *args, **kwargs):
        serializer = serializers.CreateLessonSerializer(data = request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Request Body Error."}, status=status.HTTP_400_BAD_REQUEST
                )
        serializer.is_valid(raise_exception=True)
        lesson = serializer.validated_data
        if lesson['start_date'] == "Error":
            return Response(
                {"message": "수업 시작 시간을 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST
            )
        Lesson = models.Lesson
        Log = Lessonlog
        Log.objects.create(lesson = Lesson.objects.create(title = lesson['title'],
        location = lesson['location'],
        lesson_type = lesson['lesson_type'],
        price = lesson['price'],
        personnel = lesson['personnel'],
        start_date = lesson['start_date'],
        end_date = lesson['end_date']
        ),
        reason = '생성',
        )
        return Response({"message": "수업생성 완료!"}, status = status.HTTP_200_OK)

