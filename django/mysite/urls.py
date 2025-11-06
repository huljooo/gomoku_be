from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aplikacja/', include('aplikacja.urls')),
    path('aplikacja/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('aplikacja/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
