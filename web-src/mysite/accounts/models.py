from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
import uuid


class UserManager(BaseUserManager):
    def create_user(self, username, nickname, email, password=None):
        if not username:
            raise ValueError('Users must have an username')
        if not nickname:
            raise ValueError('Users must have an name')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            useruuid=uuid.uuid4(),
            username=username,
            name=nickname,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, nickname, email, password):
        user = self.create_user(
            username=username,
            nickname=nickname,
            email=self.normalize_email(email),
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    useruuid = models.UUIDField(
        verbose_name='uuid',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    username = models.CharField(
        verbose_name='username',
        max_length=16,
        unique=True
    )
    nickname = models.CharField(
        verbose_name='nickname',
        max_length=32,
        unique=True
    )
    email = models.EmailField(
        verbose_name='email',
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
