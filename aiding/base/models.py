from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

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
    username = models.CharField(blank=False, null=False, max_length=100, unique=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

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

class Notification(models.Model):
    subject = models.CharField(blank=False, null=False, max_length=100)
    message = models.TextField(blank=False, null=False)
    targets = models.ManyToManyField(User)