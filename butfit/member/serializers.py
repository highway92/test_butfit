from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model
from .models import User, Credit
from log.models import Userlog, Lessonlog
from rest_framework_jwt.settings import api_settings
import datetime
from dateutil.relativedelta import relativedelta
from lesson.models import Lesson
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

User = get_user_model()


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserCreateSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length = 11, max_length = 11)
    nickname = serializers.CharField(min_length = 2, max_length = 10)
    password = serializers.CharField(min_length = 6, max_length = 12, write_only = True)
    verify_password = serializers.CharField(min_length = 6, max_length = 12, write_only = True)

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password", None)
        verify_password = data.get('verify_password', None)
        nickname = data.get('nickname')

        if User.objects.get(phone = phone):
            return {'phone' : 'exist'}

        if password != verify_password:
            return {'password' : 'error'}
        
        return {'phone' : phone, 'password' : password, 'nickname' : nickname}
        
        

        

class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length = 11, max_length = 11)
    password = serializers.CharField(min_length = 6, max_length = 12, write_only = True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        User = get_user_model()
        phone = data.get("phone")
        password = data.get("password", None)
        user = authenticate(data, phone=phone, password=password)
        
        if user is None:
            return {'phone': 'None'}
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
            return {
            'phone': user.phone,
            'token': jwt_token
        }

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exist'
            )

class CreditSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=6, decimal_places=0)
    phone = serializers.CharField(min_length = 11, max_length = 11)

    def validate(self, data):
        amount = data.get('amount')
        phone = data.get('phone')

        if amount > 300000:
            return {"amount" : "Error"}


        if amount < 100000:
            expiration_date = datetime.datetime.now().date() + relativedelta(months=1)
        elif 100000 <= amount < 200000:
            expiration_date = datetime.datetime.now().date() + relativedelta(months=2)
        else:
            expiration_date = datetime.datetime.now().date() + relativedelta(months=3)

        if not User.objects.get(phone = phone):
            return {'phone' : 'notexist'}
        
        return {'phone' : phone,
                    'amount' : amount,
                    'expiration' : expiration_date}

class ReserveLessonSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length = 11, max_length = 11)
    lesson_id = serializers.IntegerField()
    def validate(self, data):
        phone = data.get('phone')
        lesson_id = data.get('lesson_id')
        lesson = Lesson.objects.get(id=lesson_id)
        user = User.objects.get(phone = phone)
        credit_amount = Credit.objects.filter(user = user)
        price = lesson.price
        total = 0
        if lesson.participation.count()+1 > lesson.personnel:
            return {'lesson' : 'Error'}
        for i in lesson.participation.all():
            if i == user:
                return {'lesson' : 'Error'}
        for c in credit_amount:
            total += c.amount
        if price > total:
            return {'lesson' : 'True', 'credit' : "Error"}
        for c in credit_amount:
            if c.amount >= price:
                c.amount = c.amount - price
                c.save()
            else:
                price = price - c.amount
                c.amount = 0
                c.save()
        lesson.credit_earned = lesson.credit_earned + lesson.price
        lesson.save()
        
        lesson.participation.add(user)
        Userlog.objects.create(user = user, lesson = lesson, credit_change = -price,reason = '구매' )
        Lessonlog.objects.create(lesson = lesson, credit_change = price, reason = '구매')
        return {'lesson':'True','credit' : 'True'}

class CancelLessonSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()
    phone = serializers.CharField(min_length = 11, max_length = 11)
    def validate(self, data):
        phone = data.get('phone')
        lesson_id = data.get('lesson_id')
        lesson = Lesson.objects.get(id=lesson_id)
        user = User.objects.get(phone = phone)
        Credits = Credit.objects.filter(user = user)
        # 존재하지 않는 lesson에 대한 에러 처리
        start = lesson.start_date.date()
        today = datetime.datetime.now().date()
        flag = False
        for i in lesson.participation.all():
            if i == user:
                flag = True
                break
        if flag == False:
            return {'lesson' : 'Error', 'credit' : 'True'}

        if today <= start - datetime.timedelta(days=3):
            # 크레딧 전액 환불
            money = lesson.price
            
        elif today <= start - datetime.timedelta(days = 1):
            money = lesson.price // 2

        elif today >= start:
            return {'lesson' : 'Error', 'credit' : 'True'}
        credit = Credits[0]
        credit.amount = credit.amount + money
        credit.save()
        lesson.credit_earned = lesson.credit_earned - money
        lesson.save()
        lesson.participation.remove(user)
        Userlog.objects.create(user = user, lesson = lesson, credit_change = money ,reason = '환불' )
        Lessonlog.objects.create(lesson = lesson, credit_change = -money, reason = '환불')
        return {'lesson' : 'True', 'credit' : 'True'}

    