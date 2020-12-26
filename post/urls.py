from django.urls import path
from .views import (ListBlogPostsView, CreateBlogPostView, HomePageView)

urlpatterns = [
    path('create', CreateBlogPostView.as_view()),
    path('list', ListBlogPostsView.as_view()),
    path('home', HomePageView.as_view())
]