from django.conf.urls import url
from django.urls import path, include
from member import views
from rest_framework_jwt.views import verify_jwt_token,refresh_jwt_token


urlpatterns = [
    path('api/create-user', views.CreateUserAPI.as_view()),
    path('api/create-credit', views.CreateCreditAPI.as_view()),
    path('api/create-reservation', views.ReserveLessonAPI.as_view()),
    path('api/cancel-reservation', views.CancelLessonAPI.as_view()),
    path('api/token', views.UserLogInAPI.as_view()),
    path('api/token/verify', verify_jwt_token),
    path('api/token/refresh', refresh_jwt_token),
]