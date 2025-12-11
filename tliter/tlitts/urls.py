from django.urls import path, include
from . import api_views


urlpatterns = [

    path('register/', api_views.register),

    #                      tłity
    path('tlitts/', api_views.tlitt_list),
    path('tlitt/create/', api_views.tlitt_create),
    path('tlitt/<int:pk>/', api_views.tlitt_detail),

    #                     komentarze
    path('comments/', api_views.comment_list),
    path('comment/create/', api_views.comment_create),
    path('comment/<int:pk>/', api_views.comment_detail),

    #                     hashtagi
    path('hashtags/', api_views.hashtag_list),
    path('hashtag/create/', api_views.hashtag_create),
    path('hashtag/<int:pk>/', api_views.hashtag_detail),

    #                       like
    path('likes/', api_views.like_list),
    path('like/create/', api_views.like_create),
    path('like/<int:pk>/', api_views.like_detail),

    #                      follow
    path('follows/', api_views.follow_list),
    path('follow/create/', api_views.follow_create),
    path('follow/<int:pk>/', api_views.follow_detail),




]