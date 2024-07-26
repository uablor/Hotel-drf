from django.db import models
from common.models.base_models import Base_model
from django.db.models import Count, Sum, Avg
from django.utils.timezone import now

class Hotel(Base_model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    stars = models.PositiveSmallIntegerField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()

    def __str__(self):
        return self.name


class Staff(Base_model):
    hotel_id = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="staff_hotel"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    profile = models.ImageField(upload_to="hotel_staff/", blank=True, null=True)
    salary = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Guest(Base_model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class RoomType(Base_model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True, blank=True)
    price_per_night = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    capacity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Room(Base_model):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"

    STATUS_CHOICES = [
        (AVAILABLE, "Available"),
        (UNAVAILABLE, "Unavailable"),
    ]

    hotel_id = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="room_hotel"
    )
    room_type_id = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name="room_type"
    )
    room_number = models.CharField(max_length=15, unique=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=AVAILABLE)

    def __str__(self):
        return self.room_number


class Booking(Base_model):
    guest_id = models.ForeignKey(
        Guest, on_delete=models.CASCADE, related_name="booking_guest"
    )
    room_id = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="booking_room"
    )
    staff_id = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name="booking_staff"
    )
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.guest_id} booking for {self.room_id}"
    
    @classmethod
    def get_summary(cls):
        today = now().date()
        first_day_of_month = today.replace(day=1)
        first_day_of_year = today.replace(month=1, day=1)

        summary_today = cls.objects.filter(check_in_date=today).aggregate(
            total_bookings=Count('id'),
            total_revenue=Sum('total_price'),
            average_revenue=Avg('total_price')
        )

        summary_month = cls.objects.filter(check_in_date__gte=first_day_of_month).aggregate(
            total_bookings=Count('id'),
            total_revenue=Sum('total_price'), 
            average_revenue=Avg('total_price')
        )

        summary_year = cls.objects.filter(check_in_date__gte=first_day_of_year).aggregate(
            total_bookings=Count('id'),
            total_revenue=Sum('total_price'),
            average_revenue=Avg('total_price')
        )

        return {
            'today': summary_today,
            'month': summary_month,
            'year': summary_year
        }

   # def clean(self):
    #     super().clean()

    #     if self.check_out_date <= self.check_in_date:
    #         raise ValidationError(
    #             {"check_out_date": _("Check-out date must be after check-in date.")}
    #         )

    #     if self.check_in_date < timezone.now().date():
    #         raise ValidationError(
    #             {"check_in_date": _("Check-in date cannot be in the past.")}
    #         )

    # def save(self, *args, **kwargs):
    #     # Validate the model
    #     self.full_clean()
    #     super().save(*args, **kwargs)

class Payment(Base_model):
    PAYMENT_METHOD_CASH = "cash"
    PAYMENT_METHOD_CREDIT_CARD = "credit_card"
    PAYMENT_METHOD_DEBIT_CARD = "debit_card"
    PAYMENT_METHOD_BANK_TRANSFER = "bank_transfer"

    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_METHOD_CASH, "Cash"),
        (PAYMENT_METHOD_CREDIT_CARD, "Credit Card"),
        (PAYMENT_METHOD_DEBIT_CARD, "Debit Card"),
        (PAYMENT_METHOD_BANK_TRANSFER, "Bank Transfer"),
    ]

    booking_id = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="payment_booking"
    )
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    payment_date = models.DateField()
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, default=PAYMENT_METHOD_CASH
    )
