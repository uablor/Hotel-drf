from django.db import transaction
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView, CreateAPIView
from .models import (Hotel, Staff, Guest, RoomType, Room, Booking, Payment)
from django.db.models import Sum, Avg,Count
from .serializers import (
    HotelSerializer,
    StaffSerializer,
    GuestSerializer,
    RoomTypeSerializer,
    RoomSerializer,
    BookingSerializer,
    PaymentSerializer,
    Summary_Serializer
)

from common.mixins import SoftDeleteMixin
from rest_framework.permissions import IsAuthenticated

from .permission import (
    HotelPermission,
    StaffPermission,
    RoomTypePermission,
    RoomPermission,
    GuestPermission,
    BookingPermission,
    PaymentPermission)

class HotelViewSet(ModelViewSet, SoftDeleteMixin):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated, HotelPermission]

class StaffViewSet(ModelViewSet, SoftDeleteMixin):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated, StaffPermission]

class RoomTypeViewSet(ModelViewSet, SoftDeleteMixin):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticated, RoomTypePermission]

class RoomViewSet(ModelViewSet, SoftDeleteMixin):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, RoomPermission]

class GuestViewSet(ModelViewSet, SoftDeleteMixin):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticated, GuestPermission]

class BookingViewSet(ModelViewSet, SoftDeleteMixin):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, BookingPermission]
    def create(self, request, *args, **kwargs):
        payment_method = request.data.get("payment_method", Payment.PAYMENT_METHOD_CASH)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                self.perform_create(serializer)
                instance = serializer.instance

                # Create payment upon successful booking
                Payment.objects.create(
                    booking_id=instance,
                    amount=instance.total_price,
                    payment_date=timezone.now(),
                    payment_method=payment_method,  # Use provided payment method or default to cash
                )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PaymentViewSet(ModelViewSet, SoftDeleteMixin):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, PaymentPermission]
    

class Summary_Booking(GenericAPIView):
    def get(self, request, *args, **kwargs):
        summary = Booking.get_summary()
        return Response(summary)

class Summary_ViewSet(APIView):
    serializer_class = Summary_Serializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            bookings = Booking.objects.filter(
                check_in_date__gte=start_date,
                check_in_date__lte=end_date
            )
            
            summary = bookings.aggregate(
                total_bookings=Count('id'),
                total_revenue=Sum('total_price'),
                average_revenue=Avg('total_price')
            )

            booking_data = [{
                "first_name_guest": booking.guest_id.first_name,
                "last_name_guest": booking.guest_id.last_name,
                "room": booking.room_id.room_number,
                "name_staff": booking.staff_id.first_name + booking.staff_id.last_name,
                "check_in_date": booking.check_in_date,
                "check_out_date": booking.check_out_date,
                "total_price": booking.total_price
            } for booking in bookings]

            response_data = {
                "date":f"{start_date} - {end_date} ",
                "summary": summary,
                "bookings": booking_data
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    