from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from products.views import ProductsViewSet
from users.views.address_views import AddressViewSet
from users.views.user_views import UsersViewSet
from cart.views import CartViewSet, ItensCartViewSet
from orders.views import OrderViewSet

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='product')
router.register(r'users', UsersViewSet, basename='user')
router.register(r'address', AddressViewSet, basename='address')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'item-cart', ItensCartViewSet, basename='item-cart')
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
