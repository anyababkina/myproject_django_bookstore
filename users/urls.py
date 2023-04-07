from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', lk, name='lk'),
    path('order/', order, name='order'),
    path('orders/<int:order_id>/', AboutOrderView.as_view(), name='about_order'),
]