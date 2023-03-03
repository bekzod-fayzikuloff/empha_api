from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.booking.urls import bookings_urlpatterns, rooms_urlpatterns

from .views import RegisterViewSet

register_router = SimpleRouter()
register_router.register("", RegisterViewSet, basename="register")

docs_urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]


urlpatterns = [
    path("register/", include(register_router.urls), name="sign_up"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("bookings/", include(bookings_urlpatterns)),
    path("rooms/", include(rooms_urlpatterns)),
    path("docs/", include(docs_urlpatterns)),
]
