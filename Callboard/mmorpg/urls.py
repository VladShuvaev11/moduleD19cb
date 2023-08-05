from django.urls import path

from .views import PostList, PostDetail, PostCreate, PostEdit, PostDelete, CommentCreate, CommentDelete, Comments, \
    CommentFilter

urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/comment/', CommentCreate.as_view(), name='comment_create'),
    path('comment_accept/', Comments.as_view(), name='comment_accept'),
    path('comment/<int:pk>/delete/', CommentDelete.as_view(), name='comment_delete'),
    path('comment_filter/<int:pk>/', CommentFilter.as_view(), name='comment_filter'),

]
