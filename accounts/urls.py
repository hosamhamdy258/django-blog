from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.signUp, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', views.login, name='login'),
    path('settings/change_password/',auth_views.PasswordChangeView.as_view(template_name='accounts/changePass.html'),name='password_change'),
    path('settings/change_password/done/',auth_views.PasswordChangeDoneView.as_view(template_name='accounts/changePassDone.html'),name='password_change_done'),
    path('adminpanel', views.AdminView.as_view(), name='adminpanel'),
    path('adminpanel/allcategorys', views.AdminCategorysView.as_view(), name='all_categorys'),
    path('adminpanel/allposts', views.AdminPostsView.as_view(), name='all_posts'),
    path('adminpanel/allcomments', views.AdminCommentsView.as_view(), name='all_comments'),
    path('adminpanel/allusers', views.AdminUsersView.as_view(), name='all_users'),
    path('adminpanel/edit_category/<int:category_id>/', views.CategoryEdit.as_view(), name='edit_Category'),
    path('adminpanel/edit_post/<int:post_id>/', views.PostEditAdmin.as_view(), name='edit_Post'),
    path('adminpanel/edit_comment/<int:comment_id>/', views.CommentEdit.as_view(), name='edit_Comment'),
    path('adminpanel/post/add', views.AdminPostAddView.as_view(), name='add_Post'),
    path('adminpanel/category/add', views.AdminCategoryAddView.as_view(), name='add_Category'),
    path('adminpanel/comment/add', views.AdminCommentAddView.as_view(), name='add_Comment'),
    path('adminpanel/delete_category/<int:category_id>/', views.AdminCategoryDeleteView.as_view(), name='delete_Category'),
    path('adminpanel/delete_post/<int:post_id>/', views.AdminPostDeleteView.as_view(), name='delete_Post'),
    path('adminpanel/delete_comment/<int:comment_id>/', views.AdminCommentDeleteView.as_view(), name='delete_Comment'),
]
