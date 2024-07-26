from rest_framework import permissions
from common.basepermission import HasAnyPermission

class HotelPermission(HasAnyPermission):
    def __init__(self):
        required_permissions = {
            'GET': ['hotel.view_hotel'],
            'POST': ['hotel.add_hotel'],
            'PUT': ['hotel.change_hotel'],
            'PATCH': ['hotel.change_hotel'],
            'DELETE': ['hotel.delete_hotel']
        }
        super().__init__(required_permissions)
        
        
class StaffPermission(HasAnyPermission):
    def __init__(self):
        required_permissions = {
            'GET': ['hotel.view_staff'],
            'POST': ['hotel.add_staff'],
            'PUT': ['hotel.change_staff'],
            'PATCH': ['hotel.change_staff'],
            'DELETE': ['hotel.delete_staff']
        }
        super().__init__(required_permissions)

class RoomTypePermission(HasAnyPermission):
    def __init__(self):
        required_permissions = {
            'GET': ['hotel.view_roomtype'],
            'POST': ['hotel.add_roomtype'],
            'PUT': ['hotel.change_roomtype'],
            'PATCH': ['hotel.change_roomtype'],
            'DELETE': ['hotel.delete_roomtype']
        }
        super().__init__(required_permissions)
        
        
class RoomPermission(HasAnyPermission):
    def __init__(self):
        required_permissions = {
            'GET': ['hotel.view_room'],
            'POST': ['hotel.add_room'],
            'PUT': ['hotel.change_room'],
            'PATCH': ['hotel.change_room'],
            'DELETE': ['hotel.delete_room']
        }
        super().__init__(required_permissions)
        
    
class GuestPermission(HasAnyPermission):
    def __init__(self):
        required_permissions = {
            'GET': ['hotel.view_guest'],
            'POST': ['hotel.add_guest'],
            'PUT': ['hotel.change_guest'],
            'PATCH': ['hotel.change_guest'],
            'DELETE': ['hotel.delete_guest']
        }
        super().__init__(required_permissions)
        

class BookingPermission(HasAnyPermission):
    def __init__(self):
        self.required_permissions = {
            'GET': ['hotel.view_booking'],
            'POST': ['hotel.add_booking'],
            'PUT': ['hotel.change_booking'],
            'PATCH': ['hotel.change_booking'],
            'DELETE': ['hotel.delete_booking']
        }
        
        

class PaymentPermission(HasAnyPermission):
    def __init__(self):
        self.required_permissions = {
            'GET': ['hotel.view_payment'],
            'POST': ['hotel.add_payment'],
            'PUT': ['hotel.change_payment'],
            'PATCH': ['hotel.change_payment'],
            'DELETE': ['hotel.delete_payment']
        }
        super().__init__(self.required_permissions)


# class HotelPermission(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if request.user.is_superuser:
#             return True
#         if request.method == "GET":
#             return request.user.groups.filter(permissions__codename="view_hotel").exists()
#         if request.method == "POST":
#             return request.user.groups.filter(permissions__codename="add_hotel").exists()
#         if request.method in ["PUT", "PATCH"]:
#             return request.user.groups.filter(permissions__codename="change_hotel").exists()
#         if request.method == "DELETE":
#             return request.user.groups.filter(permissions__codename="delete_hotel").exists()
#         return False        


# class StaffPermission(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if request.user.is_superuser:
#             return True
#         if request.method == "GET":
#             return request.user.groups.filter(permissions__codename="view_staff").exists()
#         if request.method == "POST":
#             return request.user.groups.filter(permissions__codename="add_staff").exists()
#         if request.method in ["PUT", "PATCH"]:
#             return request.user.groups.filter(permissions__codename="change_staff").exists()
#         if request.method == "DELETE":
#             return request.user.groups.filter(permissions__codename="delete_staff").exists()
#         return False


# class RoomTypePermission(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if request.user.is_superuser:
#             return True
#         if request.method == "GET":
#             return request.user.groups.filter(permissions__codename="view_roomtype").exists()
#         elif request.method == "POST":
#             return request.user.groups.filter(permissions__codename="add_roomtype").exists()
#         elif request.method in ["PUT", "PATCH"]:
#             return request.user.groups.filter(permissions__codename="change_roomtype").exists()
#         elif request.method == "DELETE":
#             return request.user.groups.filter(permissions__codename="delete_roomtype").exists()
#         else :
#             return False


# class RoomPermission(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if request.user.is_superuser:
#             return True
#         if request.method == "GET":
#             return request.user.groups.filter(permissions__codename="view_room").exists()
#         elif request.method == "POST":
#             return request.user.groups.filter(permissions__codename="add_room").exists()
#         elif request.method in ["PUT", "PATCH"]:
#             return request.user.groups.filter(permissions__codename="change_room").exists()
#         elif request.method == "DELETE":
#             return request.user.groups.filter(permissions__codename="delete_room").exists()
#         else :
#             return False
       
        
# class GuestPermission(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if request.user.is_superuser:
#             return True
#         if request.method == "GET":
#             return request.user.groups.filter(permissions__codename="view_guest").exists()
#         elif request.method == "POST":
#             return request.user.groups.filter(permissions__codename="add_guest").exists()
#         elif request.method in ["PUT", "PATCH"]:
#             return request.user.groups.filter(permissions__codename="change_guest").exists()
#         elif request.method == "DELETE":
#             return request.user.groups.filter(permissions__codename="delete_guest").exists()
#         else :
#             return False
       
        
# class BookingPermission(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if request.user.is_superuser:
#             return True
#         if request.method == "GET":
#             return request.user.groups.filter(permissions__codename="view_booking").exists()
#         elif request.method == "POST":
#             return request.user.groups.filter(permissions__codename="add_booking").exists()
#         elif request.method in ["PUT", "PATCH"]:
#             return request.user.groups.filter(permissions__codename="change_booking").exists()
#         elif request.method == "DELETE":
#             return request.user.groups.filter(permissions__codename="delete_booking").exists()
#         else :
#             return False
       
        
# class PaymentPermission(permissions.BasePermission):
    
#     def has_permission(self, request, view):
#         if request.user.is_superuser:
#             return True
#         if request.method == "GET":
#             return request.user.groups.filter(permissions__codename="view_payment").exists()
#         elif request.method == "POST":
#             return request.user.groups.filter(permissions__codename="add_payment").exists()
#         elif request.method in ["PUT", "PATCH"]:
#             return request.user.groups.filter(permissions__codename="change_payment").exists()
#         elif request.method == "DELETE":
#             return request.user.groups.filter(permissions__codename="delete_payment").exists()
#         else :
#             return False