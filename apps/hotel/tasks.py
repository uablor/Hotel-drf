from celery import shared_task
from django.utils import timezone
from .models import Room, Booking

import logging

logger = logging.getLogger(__name__)
@shared_task
def update_room_status():
    try:
        today = timezone.now().date()
        expired_bookings = Booking.objects.filter(check_out_date__lt=today, room_id__status=Room.UNAVAILABLE)
        for booking in expired_bookings:
            room = booking.room_id
            room.status = Room.AVAILABLE
            room.save()
    except Exception as e:
        logger.error(f"An error occurred: {e}")