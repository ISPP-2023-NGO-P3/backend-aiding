from django.contrib.auth.models import Group, Permission, GroupManager
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.forms import ValidationError

class Contact(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100, null=False)
    message = models.TextField(max_length=1000, null=False)
    isAnswered = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def clean(self):
        if not self.phone and not self.email:
            raise ValidationError(
                "Es necesario un email o un número de teléfono")


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(
        blank=False, null=False, max_length=100, unique=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    
    roles = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    objects = UserManager()

# is_staff method used exclusively for Django admin panel, use is_admin for regular user permission.
    def is_staff(self):
        return self.is_admin

    def natural_key(self):
        return self.username

    def has_module_perms(self, perm, obj=None):
        return self.is_admin

    def has_perm(self, app_label):
        return self.is_admin

# Roles a usuarios
class GroupBaseManager(GroupManager):
    group1, created = Group.objects.get_or_create(name='supervisor')
    group2, created = Group.objects.get_or_create(name='capitan')

    permission1 = Permission.objects.get(codename='add_volunteer')
    permission2 = Permission.objects.get(codename='change_volunteer')
    permission3 = Permission.objects.get(codename='delete_volunteer')
    permission4 = Permission.objects.get(codename='view_volunteer')

    permission5 = Permission.objects.get(codename='add_turn')
    permission6 = Permission.objects.get(codename='change_turn')
    permission7 = Permission.objects.get(codename='delete_turn')
    permission8 = Permission.objects.get(codename='view_turn')
    
    for group in Group.objects.all():
        if group.name == 'supervisor':
            group.permissions.add(permission1, permission2, permission3, permission4, permission5, permission6, permission7, permission8)
        elif group.name == 'capitan':
            group.permissions.add(permission1, permission2, permission3, permission4, permission5, permission6, permission7, permission8)

class Notification(models.Model):
    subject = models.CharField(blank=False, null=False, max_length=100)
    message = models.TextField(blank=False, null=False)
    targets = models.ManyToManyField(User)
