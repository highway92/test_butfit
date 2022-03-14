from django.db import models

# Create your models here.

class Userlog(models.Model):
    user = models.ForeignKey('member.User', on_delete = models.CASCADE, null = False, db_column='user')
    lesson = models.ForeignKey('lesson.Lesson', on_delete = models.CASCADE, null = True, db_column='lesson')
    credit_change = models.IntegerField(null = False, default = 0)
    TYPE_CHOICES = (
        ('생성','유저생성'),
        ('충전','크레딧충전'),
        ('구매','수업구매'),
        ('환불','수업환불'),
    )
    reason = models.CharField(max_length = 2, choices = TYPE_CHOICES, null = False)
    log_date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.user.nickname

    class Meta:
        ordering = ['-log_date']

class Lessonlog(models.Model):
    lesson = models.ForeignKey('lesson.Lesson', on_delete = models.CASCADE, null = False, db_column='lesson')
    credit_change = models.IntegerField(null = False, default = 0)
    TYPE_CHOICES = (
        ('구매','수업구매'),
        ('환불','수업환불'),
        ('생성','수업생성')
    )
    reason = models.CharField(max_length = 2, choices = TYPE_CHOICES, null = False)
    log_date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.lesson.title

    class Meta:
        ordering = ['-log_date']