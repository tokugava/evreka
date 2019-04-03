from rest_framework import serializers
from .models import Public_Message, Poll_Choice, User_Choice, Private_Message, Public_Image, Private_Image, Site


class PublicMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Public_Message
        fields = ('id', 'subject', 'body', 'message_type', 'publish_date',
                  'expire_date', )
        
class ChoiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Poll_Choice
        fields = ('id', 'question', 'choice_text', 'votes', )
        
class PollSerializer(serializers.ModelSerializer):
    poll_choice_set = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Public_Message
        fields = ('id', 'subject', 'body', 'publish_date', 'expire_date',
                  'poll_choice_set', )

class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User_Choice
        fields = ('question', 'choice')
        
class PrivateMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Private_Message
        fields = ('id', 'subject', 'body', 'from_user', 'to_user', 'send_date', )

class WriteMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Private_Message
        fields = ('subject', 'body', )

class PublicImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Public_Image
        fields = ('id', 'image', 'message', )

class PrivateImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Private_Image
        fields = ('id', 'image', 'message', )

class SiteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Site
        fields = ('id', 'site_name', 'address', 'client_id', )