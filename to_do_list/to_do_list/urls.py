from django.contrib import admin
from django.urls import path
from rest_framework import routers
from task import views as task_views
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register(r'task', task_views.TaskViewSet, basename='task')
router.register(r'category', task_views.CategoryViewSet, basename='category')
router.register(r'user', task_views.UserViewSet, basename='user')

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('login/', views.obtain_auth_token)
]
