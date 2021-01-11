from django.urls import path
from .views import (ListBlogPostsView, CreateBlogPostView, HomePageView, StoreInPostImages, BlogPostDetailView)

urlpatterns = [
    path('create', CreateBlogPostView.as_view()),
    path('list', ListBlogPostsView.as_view()),
    path('home', HomePageView.as_view()),
    path('detail', BlogPostDetailView.as_view()),
    path('store-images', StoreInPostImages.as_view())
]