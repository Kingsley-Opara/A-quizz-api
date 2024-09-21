from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, fullname, password = None, **other_fields):
        other_fields.setdefault('is_active', True)
        # other_fields.setdefault('is_staff', True)
        # other_fields.setdefault('is_admin', False)

        if not email:
            raise ValueError('All users must have an email address')
        if not fullname:
            raise ValueError('Your Fullname is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, password=password)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, email, fullname, password = None, **other_fields):
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_staff", True)

        if not other_fields.get('active'):
            raise ValueError('All staff users must have an active account')

        user = self.create_user(
            email= email,
            fullname=fullname,
            password= password,
            **other_fields
        )
        user.save(using= self._db)
        return user
    
    def create_superuser(self, email, fullname, password =None, **other_fields):
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)

        if not other_fields.get('is_active'):
            raise ValueError('All superuser must have an active account')
        if not other_fields.get('is_staff'):
            raise ValueError('All superuser must have an active account')
        
        user = self.create_user(
            email= email,
            fullname=fullname,
            password= password,
            **other_fields
        )
        user.save(using= self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    fullname = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField( _("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=True)
    is_superuser = models.BooleanField(_("superuser status"), default=False)

    REQUIRED_FIELDS = ['fullname']
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.fullname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True