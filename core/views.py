from django.utils import timezone

from rest_framework import generics, status, permissions, response, views
from .serializers import PublicMessageSerializer, PollSerializer, VoteSerializer, PrivateMessageSerializer, WriteMessageSerializer, SiteSerializer

from .models import Public_Message, User_Choice, Poll_Choice, Private_Message, Site_User, Site

class PublicMessageList(generics.ListAPIView):
    serializer_class = PublicMessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        queryset = Public_Message.objects.all().filter(
            publish_date__lte=timezone.now(), expire_date__gte=timezone.now(), site=self.request.user.site)
        mes_type = self.request.query_params.get('message_type', None)
        if mes_type is not None:
            queryset = queryset.filter(message_type=mes_type)
        queryset = queryset.order_by('-publish_date')  
        return queryset


class PublicMessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Public_Message.objects.all()
    serializer_class = PublicMessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
class Poll(generics.RetrieveAPIView):
    serializer_class = PollSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
         queryset = Public_Message.objects.all().filter(message_type='poll', site=self.request.user.site)
         return queryset
    
class Vote(views.APIView):
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        chosen_before = User_Choice.objects.all().filter(user=request.user, 
                               choice=request.data['choice'])
        if not chosen_before:
            poll_choice = Poll_Choice.objects.get(pk=request.data['choice'])
            poll_choice.votes += 1
            poll_choice.save()
            user_choice = User_Choice()
            user_choice.user = request.user
            user_choice.question = Public_Message.objects.get(pk=request.data['question'])
            user_choice.choice = poll_choice
            user_choice.save()
            return response.Response(request.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response('Voted before', status.HTTP_400_BAD_REQUEST)
    
class PrivateMessageList(generics.ListCreateAPIView):
    serializer_class = PrivateMessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        queryset = Private_Message.objects.all().filter(
            to_user=self.request.user, site=self.request.user.site).order_by('-send_date')
        return queryset

class WriteMessage(views.APIView):
    serializer_class = WriteMessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        message = Private_Message()
        message.subject = request.data['subject']
        message.body = request.data['body']
        message.from_user = request.user
        message.to_user = Site_User.objects.get(pk=1)
        message.site = request.user.site
        message.save()
        return response.Response(request.data, status=status.HTTP_201_CREATED)

class SiteList(generics.ListAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = (permissions.AllowAny,)