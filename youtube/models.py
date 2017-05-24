# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Youtube(models.Model):
	yt_channel_id = models.CharField(max_length=100, default='Channel_ID')
	yt_video_id = models.CharField(max_length=100, unique=True)
	yt_video_title = models.CharField(max_length=200)
	yt_video_description = models.CharField(max_length = 500)



class AccessCredentials(models.Model):
	access_token = models.CharField(max_length=200, unique=True)
	refresh_token = models.CharField(max_length=200, unique=True)

