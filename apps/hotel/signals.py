from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Booking, Room, Staff


@receiver(post_save, sender=Booking)
def update_room_status_on_booking(sender, instance, created, **kwargs):
    if created:
        # Calculate the total price
        nights = (instance.check_out_date - instance.check_in_date).days
        room_type = instance.room_id.room_type_id
        instance.total_price = nights * room_type.price_per_night
        instance.save()

        # Set the room status to 'occupied'
        room = instance.room_id
        room.status = Room.UNAVAILABLE
        room.save()
        
        
# @receiver(pre_save, sender=Booking)
# def update_room_status_on_booking2(sender, instance, **kwargs):
#     if instance:
#         # Calculate the total price
#         nights = (instance.check_out_date - instance.check_in_date).days
#         room_type = instance.room_id.room_type_id
#         instance.total_price = nights * room_type.price_per_night
#         instance.save()

#         # Set the room status to 'occupied'
#         room = instance.room_id
#         room.status = Room.UNAVAILABLE
#         room.save()


# @receiver(post_save, sender=Room)
# def genNumber_roow(sender, instance, created, **kwargs):
#     if created:
#         last_room = Room.objects.all().order_by('-created_at').first()
#         if not last_room:
#             new_id = "RM-0001"
#         else:
#             last_id = last_room.room_number
#             id_num = int(last_id.split('-')[1]) + 1
#             new_id = f"BK-{id_num:04d}"

#         return Response({"booking_id": new_id}, status=status.HTTP_200_OK)


@receiver(post_delete, sender=Booking)
def update_room_status_on_checkout(sender, instance, **kwargs):
    room = instance.room_id
    room.status = Room.AVAILABLE
    room.save()
