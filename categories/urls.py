from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:category_id>', views.subscribe_unsubscribe, name='subscribe_unsubscribe'),
    path('tags/<slug:tag_slug>', views.homeTags, name='postsTags'),
    path('search/results', views.searchPosts, name='search'),
    path('new_category', views.new_category, name='new_category'),
    path('categories/<int:category_id>/', views.category_posts, name='category_posts'),
    path('categories/<int:category_id>/new/', views.new_post, name='new_post'),
    path('categories/<int:category_id>/<int:post_id>/edit', views.PostEdit.as_view(), name='editPost'),
    path('categories/<int:category_id>/<int:post_id>/', views.post, name='post'),
    path('post/<int:post_id>/like_p', views.like_post, name='like'),
    path('post/<int:post_id>/dislike_p', views.dislike_post, name='dislike'),
]
