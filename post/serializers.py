from rest_framework import serializers
from .models import (BlogPost)

class CreateBlogPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        fields = ['title', 'section', 'content', 'image', 'video']
        extra_kwargs = {'image': {'required': False}, 'video':{'required':False}}

    def create(self, validated_data):
        if(validated_data['image'] == None | validated_data['video'] == None):
            error = {'message':'Please Input either a preview video or an image'}
            raise serializers.ValidationError(error)
        return super().create(validated_data)


class BlogPostsListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BlogPost
        fields = '__all__'