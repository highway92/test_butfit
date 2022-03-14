from django.test import TestCase
from django.test import Client
from rest_framework.test import APIClient
from member.models import Credit
from lesson.models import Lesson
import unittest
from django.contrib.auth import get_user_model
import json
import datetime
User = get_user_model()

# Create your tests here.

class MemberTest(TestCase):
    def setUp(self):
        User.objects.create_user(phone = '01011111111', password = 'normalbutfit')
        normal_user = User.objects.get(phone = '01011111111')
        Lesson.objects.create(title = 'health butfitseoul', location = 'korea', lesson_type = '근력', price = '10000', personnel = '10', start_date = datetime.datetime.now()+ datetime.timedelta(days=5), end_date = datetime.datetime.now() + datetime.timedelta(days=6))
        Credit.objects.create(amount = '100000', expiration_date = datetime.datetime.now().date() + datetime.timedelta(weeks=4), user = normal_user)

    def tearDown(self):
        normal_user = User.objects.get(phone = '01011111111')
        normal_user.delete()
        
    def test_create_credit(self):
        c = Client()
        normal_user = User.objects.get(phone = '01011111111')
        normal_res = c.post('/member/api/token', {'phone' : normal_user.phone, 'password' : 'normalbutfit'})
        normal_res= json.loads(normal_res.content.decode('utf-8'))

        print('Case1 : Buying credit who does not exist Error')
        res = c.post('/member/api/create-credit',{'amount' : '50000', 'phone' : '01098765432'})
        self.assertEqual(res.status_code, 401)

        print('Case2 : Success Buying credit')
        logged_in = APIClient()
        logged_in.force_authenticate(user = normal_user)
        res = logged_in.post('/member/api/create-credit',{'amount' : '50000', 'phone' : normal_res['user']})
        self.assertEqual(res.status_code, 200)

        print('Case3 : Request body Error')
        res = logged_in.post('/member/api/create-credit',{'amount' : '50000'})
        self.assertEqual(res.status_code, 400)

        print('Case4 : Buying over 300000 Error')
        res = logged_in.post('/member/api/create-credit',{'amount' : '500000', 'phone' : normal_res['user']})
        self.assertEqual(res.status_code, 416)
        
    def test_reserve_lesson(self):
        c = Client()
        normal_user = User.objects.get(phone = '01011111111')
        logged_in = APIClient()
        logged_in.force_authenticate(user = normal_user)
        lesson = Lesson.objects.latest('id')


        print('Case1 : Success Reservation')
        res = logged_in.post('/member/api/create-reservation',{'phone' : '01011111111', 'lesson_id' : lesson.id})
        self.assertEqual(res.status_code, 200)

        print('Case2 : Reserve lesson over credit amount Error')
        lesson.price = "200000"
        lesson.save()
        res = logged_in.post('/member/api/create-reservation',{'phone' : '01011111111', 'lesson_id' : lesson.id})
        self.assertEqual(res.status_code, 403)
        lesson.price = '10000'
        lesson.save()

        print('Case3 : Reserve lesson over personnel Error')
        lesson.personnel = "0"
        lesson.save()
        self.assertEqual(res.status_code, 403)
        lesson.personnel = "10"
        lesson.save()


        print('Case4 : Duplicate Reservation Error')
        lesson.participation.add(normal_user)
        self.assertEqual(res.status_code, 403)
        lesson.participation.remove(normal_user)

    def test_cancel_lesson(self):
        c = Client()
        normal_user = User.objects.get(phone = '01011111111')
        logged_in = APIClient()
        logged_in.force_authenticate(user = normal_user)
        lesson = Lesson.objects.latest('id')
        credit = Credit.objects.latest('id')

        print('Case1 : Success Reservation Cancel')
        lesson.participation.add(normal_user)
        res = logged_in.patch('/member/api/cancel-reservation',{'phone' : '01011111111', 'lesson_id' : lesson.id})
        self.assertEqual(res.status_code, 200)

        print('Case2 : Reservation Cancel User Dose Not Exist Error')
        res = logged_in.patch('/member/api/cancel-reservation',{'phone' : '01011111111', 'lesson_id' : lesson.id})
        self.assertEqual(res.status_code, 403)

        print('Case3 : Reservation Cancel Date Error')
        lesson.participation.add(normal_user)
        lesson.start_date = datetime.datetime.now() + datetime.timedelta(days=1)
        lesson.save()
        res = logged_in.patch('/member/api/cancel-reservation',{'phone' : '01011111111', 'lesson_id' : lesson.id})
        self.assertEqual(res.status_code, 403)



        










    # def test_res(self):
    #     c = Client()
    #     normal_user = User.objects.get(phone = '01011111111')
    #     admin_user = User.objects.get(phone = '01087773624')
    #     normal_res = c.post('/member/api/token', {'phone' : normal_user.phone, 'password' : 'normalbutfit'})
    #     normal_res= json.loads(normal_res.content.decode('utf-8'))
        
