from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('register/', cache_page(60)(RegisterUserView.as_view()), name='register'),
    path('login/', cache_page(60)(LoginUserView.as_view()), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', cache_page(60 * 5)(lk), name='lk'),
    path('order/', cache_page(60)(order), name='order'),
    path('orders/<int:order_id>/', cache_page(60 * 5)(AboutOrderView.as_view()), name='about_order'),
    path('basket/<int:book_id>', add_basket, name='add_basket'),
    path('d_basket/<int:book_id>', delete_basket, name='delete_basket'),
]