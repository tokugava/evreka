from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from core import views

urlpatterns = [
    path('api/v1/public/', views.PublicMessageList.as_view()),
    path('api/v1/sites/', views.SiteList.as_view()),
    path('api/v1/public/<int:pk>/', views.PublicMessageDetail.as_view()),
    path('api/v1/polls/<int:pk>/', views.Poll.as_view()),
    path('api/v1/vote/', views.Vote.as_view()),
    path('api/v1/message/', views.WriteMessage.as_view()),
    path('api/v1/private/', views.PrivateMessageList.as_view()),
]
    
urlpatterns = format_suffix_patterns(urlpatterns)