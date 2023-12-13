from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

urlpatterns = [
    #path('', views.ticketmaster, name="ticketmaster"),
    path('', views.index, name='index'),
    path('add/', views.create_comment, name='create_comment'),
    path('update/<int:_commentid>', views.update_comment, name='update_product'),
    path('delete/<int:product_id>', views.delete_comment, name='delete_product'),
    path('search/', views.search_comment, name='search_product'),
    path('get_comments/', views.get_comments, name='get_comments'),
]
