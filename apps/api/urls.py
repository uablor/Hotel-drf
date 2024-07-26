from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LIstApiAPIview
from apps.account.views import (
    UserViewSet,
    GroupViewSet,
    PermissionViewSet,
    User_Me,
    UserTokenObtainPairView,
    UserRegisterAPIview,
    ChangePasswordAPIview,
    Send_Email_Rest_Password,
    ResetPasswordAPIView,
    VerifyEmailAPIView,
    ResendVerificationEmailAPIView,
    UserLogOutAPIView,
    
)

from apps.hotel.views import (
    HotelViewSet,
    StaffViewSet,
    RoomViewSet,
    RoomTypeViewSet,
    BookingViewSet,
    GuestViewSet,
    PaymentViewSet,
    Summary_Booking,
    Summary_ViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "api"

router = DefaultRouter()

router.register(r"user", UserViewSet, basename="user")
router.register(r"group", GroupViewSet, basename="group")
router.register(r"permission", PermissionViewSet, basename="permission")

router.register(r"hotel", HotelViewSet, basename="hotel")
router.register(r"staff", StaffViewSet, basename="staff")
router.register(r"room", RoomViewSet, basename="room")
router.register(r"roomtype", RoomTypeViewSet, basename="roomtype")
router.register(r"booking", BookingViewSet, basename="booking")
router.register(r"guest", GuestViewSet, basename="guest")
router.register(r"payment", PaymentViewSet, basename="payment")

urlpatterns = [
    
    path("", LIstApiAPIview.as_view(), name="list_api_view"),
    path("user-register/", UserRegisterAPIview.as_view(), name="user-register"),
    path("auth-login/", UserTokenObtainPairView.as_view(), name="auth-login"),
    path("auth-logout/", UserLogOutAPIView.as_view(), name="auth-logout"),
    path("auth-token-refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth-me/", User_Me.as_view(), name="auth-me"),
    path("change-password/", ChangePasswordAPIview.as_view(), name="change-password"),
    path("send-reset-password/", Send_Email_Rest_Password.as_view(), name="send-reset-password"),
    path("reset-password/<str:encoded_pk>/<str:token>/", ResetPasswordAPIView.as_view(), name="reset-password"),
    path("verify-email/", VerifyEmailAPIView.as_view(), name="verify-email"),
    path("resend-verify-email/", ResendVerificationEmailAPIView.as_view(), name="resend-verify-email"),
    path('booking-summary/', Summary_Booking.as_view(), name='booking-summary-api'),
    path('summary-viewset/', Summary_ViewSet.as_view(), name='summary-viewset'),
    
]

urlpatterns += router.urls
