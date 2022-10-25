import django, re
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        Group, PermissionsMixin, User)
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class EmployeeManager(BaseUserManager):
    """Manager for User model"""

    def create_user(self, email=None, first_name=None, last_name=None, description=None, designation=None, jod=None, passowrd=None, **Kwargs):
        """Create new user profile"""
        print(Kwargs)
        if not email:
            if len(Kwargs) > 0:
                email = Kwargs['Kwargs']['email']
        if not email :
            raise ValueError('User must have an email address!')

        regex = r'\b[A-Za-z0-9._%+-]+@ourorg.in'
        email = self.normalize_email(email)
        if re.fullmatch(regex, email):
            if not jod:
                if len(Kwargs)> 0 :
                    user = self.model(**Kwargs['Kwargs'])
                else:
                    user = self.model(email=email, first_name=first_name, last_name=last_name, description=description, designation=designation)
            else:
                user = self.model(email=email, first_name=first_name, last_name=last_name, description=description, designation=designation, jod=jod)
            user.set_password(passowrd)
            user.is_staff=True
            user.save(using=self._db)
            g,c = Group.objects.get_or_create(name='Employee')
            user.groups.add(g.id)

        else:
            raise ValueError('Not Authorized User!')
        return user
    
    def create_superuser(self, email, first_name=None, last_name=None, description=None, designation=None, jod=None, password=None):
        """Create admin user"""

        regex = r'\b[A-Za-z0-9._%+-]+admin@ourorg.in'
        if re.fullmatch(regex, email):
            user = self.create_user(email=email, first_name=first_name, last_name=last_name, description=description, designation=designation, jod=jod)
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save(using=self._db)
            g,c = Group.objects.get_or_create(name='Admin')
            user.groups.add(g.id)
        else:
            raise ValueError("Not Authorized User!")    
        return user

    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Employees(AbstractBaseUser, PermissionsMixin):
    """Store employe details"""

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    jod = models.DateField(default=django.utils.timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['email', 'first_name', 'last_name']

    def get_email(self):
        """Retrieve the email of Employee"""
        return self.email

    def get_full_name(self):
        """Get the full name of Employee"""
        return str(self.first_name) + ' ' + str(self.last_name)

    def __str__(self):
        """return string representation of the Employee"""
        return str(self.email)

    def save(self, *args, **kwargs):
        return super(Employees, self).save(*args, **kwargs)


class EmployeeLeave(models.Model):
    """Employees leave record"""
    leave_choices = (
            ('CL', 'Casual Leave'),
            ('PL', 'Privilege Leave'),
            ('SL', 'Sick Leave'),
            ('ML', 'Maternity Leave'),
            ('PTL', 'Paternity Leave')
        )

    status_choices = (
        ('A', 'Approved'),
        ('R', 'Rejected'),
        ('P', 'Pending')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=5, choices=leave_choices, default='CL')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    attachment = models.ImageField(upload_to='employee/attachment/images', null=True, blank=True)
    is_approve = models.CharField(max_length=5, choices=status_choices, default='P')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of Employee leaves"""
        return str(self.user.get_full_name() + '-' + self.leave_type)