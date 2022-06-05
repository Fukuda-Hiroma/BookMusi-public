from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid


class Inquiry(models.Model):
    inquiryuuid = models.UUIDField(
        verbose_name='inquiryuuid',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    useruuid = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='useruuid',
        on_delete=models.PROTECT
    )
    datetime = models.DateTimeField(
        verbose_name='datetime',
        default=timezone.now
    )
    title = models.CharField(
        verbose_name='title',
        max_length=64,
    )
    body = models.TextField(
        verbose_name='body',
        max_length=280,
        null=True
    )
    tags = models.CharField(
        verbose_name='tags',
        max_length=1024,
        null=True
    )
    status = models.TextField(
        verbose_name='status',
        null=True
    )

    def __str__(self):
        return self.title


class Reply(models.Model):
    replyuuid = models.UUIDField(
        verbose_name='replyuuid',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    inquiryuuid = models.ForeignKey(
        Inquiry,
        verbose_name='inquiryuuid',
        on_delete=models.CASCADE
    )
    useruuid = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='useruuid',
        on_delete=models.CASCADE
    )
    bookisbn = models.CharField(
        verbose_name='bookisbn',
        max_length=16,
    )
    datetime = models.DateTimeField(
        verbose_name='datetime',
        default=timezone.now
    )
    title = models.CharField(
        verbose_name='title',
        max_length=64,
    )
    body = models.TextField(
        verbose_name='body',
        max_length=280,
        null=True
    )
    goods = models.IntegerField(
        verbose_name='goods',
        default = 0
    )
    status = models.TextField(
        verbose_name='status',
        null=True
    )

    def __str__(self):
        return self.title


class Like(models.Model):
    replyuuid = models.ForeignKey(
        Reply,
        verbose_name='replyuuid',
        on_delete=models.CASCADE
    )
    useruuid = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='useruuid',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.replyuuid


class Checklist(models.Model):
    checkuuid = models.UUIDField(
        verbose_name='checkuuid',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    useruuid = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='useruuid',
        on_delete=models.CASCADE
    )
    bookisbn = models.CharField(
        verbose_name='bookisbn',
        max_length=16,
    )
    inquiryuuid = models.ForeignKey(
        Inquiry,
        verbose_name='inquiryuuid',
        on_delete=models.SET_NULL,
        null=True
    )
    datetime = models.DateTimeField(
        verbose_name='datetime',
        default=timezone.now
    )
    checkflag = models.BooleanField(
        verbose_name='checkflag',
        default=False
    )

    def __str__(self):
        return self.checkuuid


class Impress(models.Model):
    checkuuid = models.OneToOneField(
        Checklist,
        verbose_name='checkuuid',
        on_delete=models.CASCADE
    )
    body = models.TextField(
        verbose_name='body',
        max_length=280,
        null=True
    )
    datetime = models.DateTimeField(
        verbose_name='datetime',
        default=timezone.now
    )
    status = models.TextField(
        verbose_name='status',
        null=True
    )

    def __str__(self):
        return self.checkuuid
