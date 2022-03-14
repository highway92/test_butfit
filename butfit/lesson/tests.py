from django.test import TestCase
from django.test import Client
from rest_framework.test import APIClient
from member.models import Credit
from lesson.models import Lesson
import unittest
from django.contrib.auth import get_user_model
import json
import datetime
# Create your tests here.
User = get_user_model()

class LessonTest(TestCase):
    def setUp(self):
        User.objects.create_user(phone = '01011111111', password = 'normalbutfit')
        User.objects.create_superuser(phone = '01022222222', password = 'normalbutfit')
        normal_user = User.objects.get(phone = '01011111111')
        Lesson.objects.create(title = 'health butfitseoul', location = 'korea', lesson_type = '근력', price = '10000', personnel = '10', start_date = datetime.datetime.now()+ datetime.timedelta(days=5), end_date = datetime.datetime.now() + datetime.timedelta(days=6))
        Credit.objects.create(amount = '100000', expiration_date = datetime.datetime.now().date() + datetime.timedelta(weeks=4), user = normal_user)

    def tearDown(self):
        normal_user = User.objects.get(phone = '01011111111')
        super_user = User.objects.get(phone = '01022222222')
        super_user.delete()
        normal_user.delete()
    
    def test_check_credit(self):
        normal_user = User.objects.get(phone = '01011111111')
        logged_in = APIClient()
        logged_in.force_authenticate(user = normal_user)
        res = logged_in.get('/lesson/api/get-credit/' + str(normal_user.id))
        print('Case1 : Success Check Credit')
        self.assertEqual(res.status_code, 200)
    
    def test_check_lesson(self):
        normal_user = User.objects.get(phone = '01011111111')
        logged_in = APIClient()
        logged_in.force_authenticate(user = normal_user)
        res = logged_in.get('/lesson/api/get-lesson/' + str(normal_user.id))
        print('Case1 : Success Check Lesson')
        self.assertEqual(res.status_code, 200)

    def test_create_lesson(self):
        super_user = User.objects.get(phone = '01022222222')
        logged_in = APIClient()
        logged_in.force_authenticate(user = super_user)
        print('Case1 : Success Create Lesson')
        res = logged_in.post('/lesson/api/create-lesson', {
  "title": "테스트 수업",
  "location": "서울시 강남구",
  "lesson_type": "유산소",
  "price": "50000",
  "personnel": "10",
  "start_date": "2022-03-15T06:43:14.921Z",
  "end_date": "2022-03-17T06:43:14.921Z"
})
        self.assertEqual(res.status_code, 200)

        print('Case2 : Validation Error')
        res = logged_in.post('/lesson/api/create-lesson', {
  "title": "테스트 수업",
  "location": "서울시 강남구",
  "lesson_type": "필라테스후 유산소",
  "price": "50000",
  "personnel": "10",
  "start_date": "2022-03-15T06:43:14.921Z",
  "end_date": "2022-03-17T06:43:14.921Z"
})
        self.assertEqual(res.status_code, 400)

        