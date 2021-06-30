from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from django.core.mail import send_mail
from .serializers import (CreateBlogPostSerializer, 
BlogPostsListSerializer, BlogPostsDetailSerializer, InPostImagesSerializer,
ContactSerailizer)
from django.conf import settings
from rest_framework.parsers import FileUploadParser
from .models import BlogPost
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_cookie


class PageNumberPaginationWithCount(PageNumberPagination):
    
    def get_paginated_response(self, data):
        response = super(PageNumberPaginationWithCount, self).get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        response.data['current'] = self.page.number
        response.data['prev_page_number'] = None
        response.data['next_page_number'] = None
        if self.page.has_previous():
            response.data['prev_page_number'] = self.page.previous_page_number()
        if self.page.has_next():
            response.data['next_page_number'] = self.page.next_page_number()
        # response['headers']['Cache-Control'] = 'no-cache, max-age=10400'
        return response

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
    
    @method_decorator(cache_page(60*60*60*4))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        paginator = PageNumberPaginationWithCount()
        paginator.page_size = 8
        if request.query_params['section'] == 'VIDEOS':
            posts = BlogPost.objects.exclude(video='').order_by('-posted')
        else:
            posts = BlogPost.objects.filter(section=request.query_params['section']).order_by('-posted')
        result_page = paginator.paginate_queryset(posts, request)
        latest_post = BlogPost.objects.last()

        serializer = BlogPostsListSerializer(result_page, many=True)
        latest_post_serializer = BlogPostsListSerializer(latest_post, many=False)
        data = paginator.get_paginated_response(serializer.data)
        return data


class HomePageView(ListAPIView):

    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        latest_post = BlogPost.objects.last()
        enterntainment_posts = BlogPost.objects.filter(section='ENTERTAINMENT').order_by('-posted')[:3]
        crime_posts = BlogPost.objects.filter(section='CRIME').order_by('-posted')[:3]
        politics_posts = BlogPost.objects.filter(section='POLITICS').order_by('-posted')[:3]
        romance_posts = BlogPost.objects.filter(section='ROMANCE').order_by('-posted')[:3]
        headlines = BlogPost.objects.order_by('-posted')[1:4]

        latest_serializer = BlogPostsListSerializer(latest_post, many=False)
        headlines_serializer = BlogPostsListSerializer(headlines, many=True)
        entertainment_serializer = BlogPostsListSerializer(enterntainment_posts, many=True)
        crime_serializer = BlogPostsListSerializer(crime_posts, many=True)
        politics_serializer = BlogPostsListSerializer(politics_posts, many=True)
        romance_serializer = BlogPostsListSerializer(romance_posts, many=True)

        data = {
            'latest':latest_serializer.data,
            'headlines': headlines_serializer.data,
            'entertainment':entertainment_serializer.data,
            'business':crime_serializer.data,
            'politics':politics_serializer.data,
            'romance':romance_serializer.data
        }

        return Response(data, status=status.HTTP_200_OK, headers={'Cache-Control':'no-cache'})


# class StoreInPostImages(CreateAPIView):
#     parser_class = (FileUploadParser,)

#     def post(self, request, *args, **kwargs):
#         serializer = InPostImagesSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             obj = serializer.save()
#             data = {'url': obj.upload.url}
#             return Response(data, status=status.HTTP_201_CREATED)

class ContactView(APIView):
    def post(self, request, *args, **kwargs):
        serailizer_class = ContactSerailizer(data=request.data)
        if serailizer_class.is_valid(raise_exception=True):
            data = serailizer_class.validated_data
            email_from = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(subject, message, email_from, [settings.EMAIL_HOST_USER, ])
            return Response({"success": "Sent"})
        return Response({'success': "Failed"}, status=status.HTTP_400_BAD_REQUEST)


class BlogPostDetailView(ListAPIView):

    # @method_decorator(cache_page(60*60*60*4))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        slug = request.query_params['slug']
        try:
            post = BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            return Response({'message':'POST_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogPostsDetailSerializer(post, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK, headers={'Cache-Control':'no-cache'})
