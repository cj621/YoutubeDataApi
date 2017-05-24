# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db import IntegrityError

from .models import Youtube

from django.http import HttpResponse

from oauth2client import client
from apiclient.discovery import build
import json, httplib2

from .models import AccessCredentials, Youtube



flow = client.flow_from_clientsecrets(
    'client_secrets.json',
    scope='https://www.googleapis.com/auth/youtube.readonly',
    redirect_uri='http://localhost:8000/youtube')
flow.params['access_type'] = 'offline'         # offline access
# flow.params['include_granted_scopes'] = True   # incremental auth


def index(request):
	auth_uri = flow.step1_get_authorize_url()
	if request.GET.get('code'):
		code = request.GET.get('code')
		credentials = flow.step2_exchange(code)
		http_auth = credentials.authorize(httplib2.Http())

		acc_tok = AccessCredentials(access_token=credentials, refresh_token=http_auth)
		try:
			acc_tok.save()
		except IntegrityError as e:
			pass
		else:
			pass


		youtube = build('youtube', 'v3', http=http_auth)
		channel = youtube.channels().list(mine=True ,part="id, contentDetails, snippet").execute()

		channel_id = channel['items'][0]['id']

		uploads_list_id = channel['items'][0]["contentDetails"]["relatedPlaylists"]["uploads"]


		# Retrieve the list of videos uploaded to the authenticated user's channel.
	  	playlistitems_list_request = youtube.playlistItems().list(
	  		playlistId=uploads_list_id,
	  		part="snippet")

	  	counter = 0
	  	while counter<1:
	  		playlistitems_list_response = playlistitems_list_request.execute()
	  		counter += 1


	  	for playlist_item in playlistitems_list_response['items']:
	  		video_id = playlist_item['snippet']['resourceId']['videoId']
	  		title = playlist_item['snippet']['title']
	  		description = playlist_item['snippet']['description']
	  		video_details = Youtube(yt_channel_id=channel_id , yt_video_id=video_id, yt_video_title=title, yt_video_description=description)
	  		try:
	  			video_details.save()
	  		except IntegrityError as e:
	  			pass
	  		else:
	  			pass
	  		
	  	youtube_videos = Youtube.objects.filter(yt_channel_id=channel_id)

		return render(request, 'youtube/data.html', {'youtube_videos': youtube_videos })
	elif request.GET.get('view'):
		channel_id = request.GET.get('view')
		list_of_videos = Youtube.objects.filter(yt_channel_id=channel_id)
		return render(request, 'youtube/data.html', {'youtube_videos': list_of_videos })
	else:
		return render(request, 'youtube/index.html', { 'auth_uri': auth_uri })


### Details of the each individual Video
def detail(request, v_id):
	yt_video_details = Youtube.objects.filter(yt_video_id=v_id)
	return render(request, 'youtube/detail.html', {'yt_video_details': yt_video_details})
