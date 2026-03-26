from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('realtor/<int:realtor_id>/', views.realtor_detail, name='realtor_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # API endpoints
    path('api/call-request/', views.call_request_api, name='call_request_api'),
    path('api/payment/', views.payment_api, name='payment_api'),
]
