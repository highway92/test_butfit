from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
import datetime
from dateutil.relativedelta import relativedelta

class CreateLessonSerializer(serializers.Serializer):
    title = serializers.CharField(max_length = 30)
    location = serializers.CharField(max_length = 255)
    lesson_type = serializers.CharField(max_length = 5)
    price = serializers.DecimalField(max_digits=6, decimal_places=0)
    personnel = serializers.DecimalField(max_digits=2, decimal_places=0)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    def validate(self, data):
        title = data.get('title')
        location = data.get('location')
        lesson_type = data.get('lesson_type')
        price = data.get('price')
        personnel = data.get('personnel')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date > end_date:
            return {'start_date' : 'Error'}
        
        return {'title':title,
        'location':location,
        'lesson_type':lesson_type,
        'price':price,
        'personnel':personnel,
        'start_date':start_date,
        'end_date':end_date}