from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import (CreateBlogPostSerializer, BlogPostsListSerializer)
from rest_framework.parsers import FileUploadParser
from .models import BlogPost

class CreateBlogPostView(CreateAPIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        serializer = CreateBlogPostSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {'message':'Post successfully created!'}
            return Response(data, status=status.HTTP_201_CREATED)

        else:
            data = {'message':'An Error Occured'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class ListBlogPostsView(ListAPIView):

    def list(self, request, *args, **kwargs):
        posts = BlogPost.objects.filter(section=request.query_params['section'])
        serializer = BlogPostsListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HomePageView(ListAPIView):

    def list(self, request, *args, **kwargs):
        latest_post = BlogPost.objects.last()
        enterntainment_posts = BlogPost.objects.filter(section='ENTERTAINMENT').order_by('-posted')[:3]
        fashion_posts = BlogPost.objects.filter(section='FASHION').order_by('-posted')[:3]
        news_posts = BlogPost.objects.filter(section='NEWS').order_by('-posted')[:3]
        crime_posts = BlogPost.objects.filter(section='CRIME').order_by('-posted')[:3]

        latest_serializer = BlogPostsListSerializer(latest_post, many=False)
        entertainment_serializer = BlogPostsListSerializer(enterntainment_posts, many=True)
        fashion_serializer = BlogPostsListSerializer(fashion_posts, many=True)
        news_serializer = BlogPostsListSerializer(news_posts, many=True)
        crime_serializer = BlogPostsListSerializer(crime_posts, many=True)

        data = {
            'latest':latest_serializer.data(),
            'entertainment':entertainment_serializer.data(),
            'fashion':fashion_serializer.data(),
            'news':news_serializer.data(),
            'crime':crime_serializer.data()
        }

        return Response(data, status=status.HTTP_200_OK)
