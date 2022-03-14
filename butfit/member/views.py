from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth import get_user_model
from member import serializers
from log.models import Userlog
from member.models import Credit
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from drf_yasg             import openapi 


from drf_yasg.utils       import swagger_auto_schema

# Create your views here.

@permission_classes([AllowAny])
class CreateUserAPI(APIView):
    @swagger_auto_schema(request_body=serializers.UserCreateSerializer)
    def post(self, request, *args, **kwargs):
        serializer = serializers.UserCreateSerializer(data = request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT
                )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user['phone'] == 'exist' or user['password'] == 'error':
            return Response(
                {"message": "회원가입에 실패했습니다. 아이디와 비밀번호를 확인해주세요."}, status=status.HTTP_409_CONFLICT
            )
        User = get_user_model()
        User.objects.create_user(phone=user['phone'], password=user['password'])
        new_user = User.objects.get(phone = user['phone'])
        new_user.nickname = user['nickname']
        new_user.save()
        return Response({"message": "회원가입 완료!"}, status = status.HTTP_200_OK)


@permission_classes([AllowAny])
class UserLogInAPI(APIView):
    @swagger_auto_schema(request_body=serializers.UserLoginSerializer)
    # @transaction.atomic
    # https://brownbears.tistory.com/573 확인해보기
    def post(self, request, *args, **kwargs):
        serializer = serializers.UserLoginSerializer(data = request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT
                )

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user['phone'] == "None":
            return Response(
                {"message": "로그인이 실패했습니다. 아이디와 비밀번호를 확인해주세요."}, status=status.HTTP_401_UNAUTHORIZED
                )
        
        return Response(
            {
                "user": user['phone'], 
                "token": user['token']
            }, status = status.HTTP_200_OK
        )

@permission_classes([IsAuthenticated])
class CreateCreditAPI(APIView):
    @swagger_auto_schema(request_body=serializers.CreditSerializer)
    def post(self, request, *args, **kwargs):
        serializer = serializers.CreditSerializer(data = request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Request Body Error."}, status=status.HTTP_400_BAD_REQUEST
                )

        serializer.is_valid(raise_exception=True)
        credit = serializer.validated_data
        if credit['amount'] == 'Error':
            return Response(
                {"message": "크레딧 구매는 30만원을 초과할 수 없습니다."}, status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
            )
        elif credit['phone'] == 'notexist':
            return Response(
                {"message": "유저가 존재하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            User = get_user_model()
            user = User.objects.get(phone = credit['phone'])
            Userlog.objects.create(user = user, credit_change = credit['amount'], reason = '충전')
            Credit.objects.create(amount = credit['amount'], expiration_date = credit['expiration'], user = user)
            return Response({"message": "크레딧 구매 완료!" }, status = status.HTTP_200_OK)
            
        

@permission_classes([IsAuthenticated])
class ReserveLessonAPI(APIView):
    @swagger_auto_schema(request_body=serializers.ReserveLessonSerializer, responses={200: 'Success'})
    def post(self, request, *args, **kwargs):
        serializer = serializers.ReserveLessonSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        reservation = serializer.validated_data

        if reservation['lesson'] == 'Error' or reservation['credit'] == 'Error':
            return Response(
                {"message": "오류가 발생했습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        return Response({"message": "수업 예약 완료!"},status = status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class CancelLessonAPI(APIView):
    @swagger_auto_schema(request_body=serializers.CancelLessonSerializer, responses={200: 'Success'})
    def patch(self, request, *args, **kwargs):
        serializer = serializers.CancelLessonSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        cancel = serializer.validated_data
        if cancel['lesson'] == 'Error':
            return Response(
                {"message": "오류가 발생했습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        return Response({"message": "수업 취소 완료!"},status = status.HTTP_200_OK)
