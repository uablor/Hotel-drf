from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response


class LIstApiAPIview(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "auth": {

                "auth me": reverse("api:auth-me", request=request),
                "login user": reverse("api:auth-login", request=request),
                "logout user": reverse("api:auth-logout", request=request),
                "token refresh": reverse("api:token-refresh", request=request),
                "user register": reverse("api:user-register", request=request, format=None),
                
                "custom password":{
                "change password": reverse("api:change-password", request=request),
                "send reset password": reverse("api:send-reset-password", request=request),
                "reset password": reverse("api:reset-password", kwargs={"encoded_pk": "<encoded_pk>", "token": "<token>"}, request=request, format=None),
                },
                "verify email":{
                "resend verify email" : reverse("api:resend-verify-email", request=request, format=None),
                "verify email": reverse("api:verify-email", request=request, format=None),
                },

                

            },
           
            "account": {
                "user": reverse("api:user-list", request=request, format=None),
                "group": reverse("api:group-list", request=request, format=None),
                "permission": reverse("api:permission-list", request=request, format=None),
            },
            "hotel":{
                "hotel": reverse("api:hotel-list", request=request, format=None),
                "staff": reverse("api:staff-list", request=request, format=None),
                "guest": reverse("api:guest-list", request=request, format=None),
                "room": reverse("api:room-list", request=request, format=None),
                "roomtype": reverse("api:roomtype-list", request=request, format=None),
                "booking": reverse("api:booking-list", request=request, format=None),
                "payment": reverse("api:payment-list", request=request, format=None),
                "summary booking": reverse("api:booking-summary-api", request=request, format=None),
                "summary viewset": reverse("api:summary-viewset", request=request, format=None),
            },
        }
        return Response(data)
