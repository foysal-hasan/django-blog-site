from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'), 
    path('post/new/', views.post, name='new_post'), 
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'), 
    path('post/drafts', views.post_draft_list, name='post_draft_list'), 
    path('post/delete/<int:pk>', views.post_delete, name='delete_post'), 
    path('post/my_posts', views.my_posts, name='my_posts'), 
    path('post/<int:pk>/publish', views.post_publish, name='post_publish'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signUp, name='signup'),
    path('password_change/', views.password_change, name='password_change'),

    # http://127.0.0.1:8000/post/10/comment/add
    path('post/<int:pk>/comment/add', views.add_comment_on_post, name='add_comment'), 
    # http://localhost:8000/post/10/comment/delete
    path('post/<int:pk>/comment/delete', views.delete_comment, name='delete_comment'),

]
