from django.urls import path

from . import views

urlpatterns = [
    path('', views.create_posts_view, name='posts'),
    path('edit_post/<int:pk>', views.EditPostView.as_view(), name='edit_post'),
    path('remove_post/<int:pk>', views.DeletePostView.as_view(), name='remove_post'),
]
