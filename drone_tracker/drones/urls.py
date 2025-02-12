from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', views.get, name='get-all-drones'),
    path('dangerous/', views.get_all_dangerous_drones, name='get-all-dangerous-drones'),
    path('online/', views.get_all_online_drones, name='get-all-online-drones'),
    path('serial/<str:serial>/', views.get_drone_by_serial, name='get-drone-by-serial'),
    path('<int:drone_id>/', views.get_by_id, name='get-drone-by-id'),
    path('flight-path/<str:serial>/', views.get_drone_flight_path, name='get-drone-flight-path'),
    path("nearby/", views.get_nearby_drones, name="drones_nearby"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.create_user, name='create-user'),
    path('login/', views.login, name='login'),


]