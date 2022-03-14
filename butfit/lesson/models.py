from django.db import models
import datetime
# Create your models here
class Lesson(models.Model):
    title = models.CharField(max_length = 30, null=False)
    location = models.CharField(max_length = 255, null = False)
    TYPE_CHOICES = (
        ('유산소','유산소운동'),
        ('근력','근력운동'),
    )
    credit_earned = models.DecimalField(max_digits=10, decimal_places=0, default = 0, null = False)
    lesson_type = models.CharField(max_length = 3, choices = TYPE_CHOICES, null = False) 
    price = models.DecimalField(max_digits=6, decimal_places=0)
    personnel = models.DecimalField(max_digits=2, decimal_places=0)
    start_date = models.DateTimeField(null = False)
    end_date = models.DateTimeField(null=False)
    participation = models.ManyToManyField('member.User', related_name = 'users', db_column='participation', blank = True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['location']