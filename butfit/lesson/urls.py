from django.conf.urls import url
from django.urls import path, include
from lesson import views


urlpatterns = [
    path('api/create-lesson', views.CreateLessonAPI.as_view()),
    path('api/get-credit/<int:user_id>', views.CheckCreditAPI.as_view()),
    path('api/get-lesson/<int:user_id>', views.CheckLessonAPI.as_view()),
]