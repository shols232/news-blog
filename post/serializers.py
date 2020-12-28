from rest_framework import serializers
from .models import (BlogPost)

class CreateBlogPostSerializer(serializers.ModelSerializer):


    class Meta:
        model = BlogPost
        fields = ['title', 'section', 'content', 'image', 'video']
        extra_kwargs = {'image': {'required': False}, 'video':{'required':False}}

    def create(self, validated_data):
        try:
            if(validated_data['image'] != None):
                    return super().create(validated_data)
        except KeyError:
            pass
        try:
            if(validated_data['video'] != None):
                return super().create(validated_data)
        except KeyError:
            error = {'message':'Please Input either a preview video or an image'}
            raise serializers.ValidationError(error)


class BlogPostsListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BlogPost
        fields = '__all__'