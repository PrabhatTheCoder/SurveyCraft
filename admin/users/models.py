from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid



class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('OWN', 'Owner'),
        ('MNG', 'Manager'),
    )
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=3, choices=USER_TYPE_CHOICES)
    
    managed_contestants = models.ManyToManyField('self', limit_choices_to={'user_type': 'CNT'}, blank=True, related_name='managed_by', symmetrical=False)
    
    project = models.ManyToManyField("Project", blank=True) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.name


class AppUsers(models.Model):
    
    SOURCE_CHOICES = (
     ('clevertap', 'CleverTap'),
     ( 'moengage', 'MoEngage'),
    )
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, null=True, blank=True)
    app = models.ForeignKey('appinfo.App', on_delete=models.CASCADE, related_name='appUsers')
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES, null=True, blank=True)
    extra_attributes = models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id', 'app')