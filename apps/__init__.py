import uuid

from base.constants import DEFAULT_USER_PASSWORD
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models
from django_countries.fields import CountryField


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    phone_md5 = models.CharField(max_length=255, null=True, blank=True, unique=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    point = models.IntegerField(default=0)
    is_new_user = models.BooleanField(default=True)
    country = CountryField(null=True, blank=True)

    email = None
    is_staff = None
    first_name = None
    last_name = None
    is_superuser = None

    class Meta:
        db_table = "users"
        app_label = "authentication"

    def save(self, *args, **kwargs):
        self.username = self.username
        self.password = self.encode_password(self.password)

        super().save(*args, **kwargs)
        cache.set(f"user_{self.id}", self)

    def generate_random_username(self):
        new_username = "user_" + str(uuid.uuid4())[:8]
        if User.objects.filter(username=new_username).exists():
            return self.generate_random_username()
        return new_username

    def encode_password(self, password):
        encoded_password = make_password(password)
        return encoded_password

    @classmethod
    def get_by_id(cls, id):
        user = cache.get(f"user_{id}")
        if not user:
            user = cls.objects.get(id=id)
            cache.set(f"user_{id}", user)

        return user
