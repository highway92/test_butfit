from django.contrib import admin
from .models import Userlog,Lessonlog
from rangefilter.filter import DateRangeFilter
from lesson.models import Lesson
# Register your models here.
admin.site.register(Userlog)

class LessonlogAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'credit_change', 'log_date')
    list_filter = (
        ('log_date',DateRangeFilter),'lesson'
        )
    search_fields = ("^lesson__id",)
     
admin.site.register(Lessonlog, LessonlogAdmin)
