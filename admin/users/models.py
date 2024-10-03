from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from django.contrib.auth.hashers import make_password



# *******   [ JWT or OAuth will be use in Future ] ********
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
    
    role = models.CharField(choices=USER_TYPE_CHOICES, max_length=50)
    app = models.ManyToManyField('company.app', related_name="users", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_banned = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.name
    
    def is_admin_allowed(self, app):
        return self.role == "owner" and app in self.app.all()
    


class AppUsers(models.Model):
    
    SOURCE_CHOICES = (
     ('clevertap', 'CleverTap'),
     ( 'moengage', 'MoEngage'),
    )
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, null=True, blank=True)
    
    password = models.CharField(max_length=128, null=False, blank=True)
    
    app = models.ForeignKey('company.App', on_delete=models.CASCADE, related_name='appUsers')
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES, null=True, blank=True)
    extra_attributes = models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def set_password(self, raw_password):
        related_audiences = self.audience_set.filter(projects__projectType='QUZ')
        if not related_audiences.exists():
            return 
        self.password = make_password(raw_password)
        self.save()

    class Meta:
        unique_together = ('id', 'app')
        
        
    def __str__(self):
        return self.name or 'Anonymous App User'