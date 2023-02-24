from rest_framework.routers import SimpleRouter

from . import views

rooms_router = SimpleRouter()
rooms_router.register("", views.RoomViewSet, basename="room")

bookings_router = SimpleRouter()
bookings_router.register("", views.BookingViewSet, basename="booking")

rooms_urlpatterns = []
bookings_urlpatterns = []


rooms_urlpatterns += rooms_router.urls
bookings_urlpatterns += bookings_router.urls
