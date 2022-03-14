from member import Credit

def delete_expired():
    now = timezone.now()
    Credit.objects.filter(expire_time__lt=now).delete()