from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError('Users must have an phone number')

        user = self.model(
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
# make user
    username = None
    phone_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$", message="Phone number must be entered in the format: '01099999999'. Up to 11 digits allowed.")
    phone = models.CharField(_('phone number'), validators=[phone_regex], max_length=11, unique=True) # validators should be a list
    nickname = models.CharField(max_length = 10, null = False, default = '익명유저')
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.phone
    
    def has_perm(self, perm, obj = None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

class Credit(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=0)
    expiration_date = models.DateField(null = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_phone', db_column='user')

    def __str__(self):
        return str(self.amount)
    
    class Meta:
        ordering = ['expiration_date']