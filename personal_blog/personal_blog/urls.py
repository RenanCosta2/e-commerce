from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from post import views as post_views
from user import views as user_views
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register(r'post', post_views.PostViewSet, basename='post')
router.register(r'user', user_views.CustomUserViewSet, basename='user')

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('login/', views.obtain_auth_token),
    path('logout/', user_views.logout_user)
]
