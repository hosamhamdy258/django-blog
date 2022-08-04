from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.signUp, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('settings/change_password/',auth_views.PasswordChangeView.as_view(template_name='accounts/changePass.html'),name='password_change'),
    path('settings/change_password/done/',auth_views.PasswordChangeDoneView.as_view(template_name='accounts/changePassDone.html'),name='password_change_done'),
    path('adminpanal', views.AdminView.as_view(), name='adminpanal'),
    path('adminpanal/allcategorys', views.AdminCategorysView.as_view(), name='all_categorys'),
    path('adminpanal/allposts', views.AdminPostsView.as_view(), name='all_posts'),
    path('adminpanal/allcomments', views.AdminCommentsView.as_view(), name='all_comments'),
    path('adminpanal/allusers', views.AdminUsersView.as_view(), name='all_users'),
    path('adminpanal/edit_category/<int:category_id>/', views.CategoryEdit.as_view(), name='edit_Category'),
    path('adminpanal/edit_post/<int:post_id>/', views.PostEditAdmin.as_view(), name='edit_Post'),
    path('adminpanal/edit_comment/<int:comment_id>/', views.CommentEdit.as_view(), name='edit_Comment'),
    path('adminpanal/post/add', views.AdminPostAddView.as_view(), name='add_Post'),
    path('adminpanal/category/add', views.AdminCategoryAddView.as_view(), name='add_Category'),
    path('adminpanal/comment/add', views.AdminCommentAddView.as_view(), name='add_Comment'),
    path('adminpanal/delete_category/<int:category_id>/', views.AdminCategoryDeleteView.as_view(), name='delete_Category'),
    path('adminpanal/delete_post/<int:post_id>/', views.AdminPostDeleteView.as_view(), name='delete_Post'),
    path('adminpanal/delete_comment/<int:comment_id>/', views.AdminCommentDeleteView.as_view(), name='delete_Comment'),

]
