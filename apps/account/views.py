from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, GenericAPIView
from .models import User
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializer import (
    GroupSerialiazer,
    PermissionSerializer,
    UserSerializer,
    UserTokenObtainPairSerializer,
    UserRegisterSerializer,
    ChangePasswordSerializer,
    EmailSerializer,
    ResetPasswordSerializer,
    LogOutSerializer
)

from rest_framework.response import Response
from django.core.mail import send_mail

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from common.mixins import SoftDeleteMixin
from .permission import (
    GroupPermission,
    PermissionPermission,
    UserPermission
)
from django.contrib.auth import logout as django_logout
# from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import logging
from common.viewsets.base_viewsets import BaseModelviwSet

logger = logging.getLogger(__name__)


class UserLogOutAPIView(APIView):
    serializer_class  = LogOutSerializer
    def post(self, request, *args, **kwargs):
        django_logout(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)  # Raise exception on validation failure
        return Response({"message": "Logout successfully."}, status=status.HTTP_204_NO_CONTENT)


class UserTokenObtainPairView(TokenObtainPairView):
    
    serializer_class = UserTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.user
            response.data["user_id"] = user.id
            response.data["email"] = user.email
            response.data["user_fullname"] = user.first_name + user.last_name
            # response.data["is_verified"] = user.is_verify
        return response


class UserViewSet(BaseModelviwSet, SoftDeleteMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]
    
    # def get_queryset(self):
    #     # For normal operations, use the default queryset
    #     if self.action in ['restore', 'hard_delete']:
    #         return User.all_objects.all()
    #     return User.objects.all()

    # def get_object(self):
    #     # Override to fetch from all_objects
    #     queryset = self.filter_queryset(self.get_queryset())
    #     obj = queryset.get(pk=self.kwargs["pk"])
    #     self.check_object_permissions(self.request, obj)
    #     return obj

    # def _get_user_or_404(self, pk):
    #     try:
    #         user = User.all_objects.get(pk=pk)
    #         self.check_object_permissions(self.request, user)
    #         return user
    #     except User.DoesNotExist:
    #         raise Http404("User not found")

    # @action(detail=False, methods=['get'], url_path='soft-delete')
    # def soft_delete(self, request):
    #     deleted_users = User.deleted_objects.all()

    #     # Paginate the queryset of deleted instances
    #     page = self.paginate_queryset(deleted_users)

    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(deleted_users, many=True)
    #     return Response(serializer.data)

    # @action(detail=True, methods=['post'], url_path='restore')
    # def restore(self, request, pk=None):
    #     user = self._get_user_or_404(pk)
        
    #     if user.is_deleted:
    #         user.restore()
    #         return Response({'status': 'user restored'}, status=status.HTTP_200_OK)
    #     return Response({'status': 'user is not deleted'}, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['delete'], url_path='hard-delete')
    # def hard_delete(self, request, pk=None):
    #     user = self._get_user_or_404(pk)

    #     user.hard_delete()
    #     return Response({'status': 'user permanently deleted'}, status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerialiazer
    permission_classes = [GroupPermission]


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [PermissionPermission]


class User_Me(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserRegisterAPIview(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class ChangePasswordAPIview(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated, UserPermission]
    
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response({"status": "password set ... "}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Send_Email_Rest_Password(APIView):
    
    serializer_class = EmailSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            # Generate token and reset link
            encoded_pk = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)
            reset_url = reverse("api:reset-password", kwargs={"encoded_pk": encoded_pk, "token": token})
            reset_link = f"http://localhost:8000{reset_url}"
            subject = 'Password Reset Request'
            message = f'Hi {user.username},\n\nPlease click the link below to reset your password:\n\n{reset_link}'
            
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]
    def put(self, request, encoded_pk, token):
        user_id = force_str(urlsafe_base64_decode(encoded_pk))
        user = User.objects.get(pk=user_id)
        
        if default_token_generator.check_token(user, token):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({"message": "Password reset complete"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"error": "Invalid token or user"}, status=status.HTTP_400_BAD_REQUEST)
    
    # def post(self, request, *args, **kwargs):
    #     serializer = ResetPasswordSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class VerifyEmailAPIView(APIView):
    
    permission_classes = [ AllowAny]
    def get(self, request, *args, **kwargs):
        uid = request.query_params.get('uid')
        token = request.query_params.get('token')
        if uid is None or token is None:
            return Response({'error': 'Missing uid or token'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_verify = True
            user.save()
            return Response({'detail': 'Email successfully verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)
        

class ResendVerificationEmailAPIView(APIView):
    serializer_class = EmailSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            if user.is_verify == True:
                return Response({'message': 'Email is already verified.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                subject = 'Verify Your Email Address'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                verify_url = f"http://localhost:8000{reverse('api:verify-email')}?uid={uid}&token={token}"

                context = {
                    'user': user,
                    'verify_url': verify_url,
                }
                convert_to_html_content =  render_to_string(
                template_name="verification_email.html",
                context = context
                )
                
                plain_message = strip_tags(convert_to_html_content)
                a = send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],   # recipient_list is self explainatory
                html_message=convert_to_html_content,
                fail_silently=True,   # Optional
                ) 
                return Response({'message': 'Verification email resent successfully.'}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f'Error sending email: {e}')
                print(f'Error sending email: {e}')
                '''Use the django.core.mail.send_mail function indicating in the html_message parameter the result of having rendered the template, something like this:
# quickly example of sending html mail
from django.core.mail import send_mail
from django.template.loader import get_template


# I preferred get_template(template).render(context) you can use render_to_string if you want

context = {'first_name': 'John', 'last_name': 'Devoe'}
template = get_template('my_custom_template.html').render(context)

send_mail(
    'Custom Subject',
    None, # Pass None because it's a HTML mail
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
    html_message = template
)'''
                
                '''# text_content = f'Hi {user.first_name},\n\nPlease verify your email address by clicking the following link:\n\n{verify_url}'
                # send_mail(subject, None,settings.DEFAULT_FROM_EMAIL, [user.email] , fail_silently=False,
                # html_message = template)
                # msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                # logger.error(f'{msg}')'''
                
                '''# msg = EmailMultiAlternatives(
                #     subject,
                #     None, # This is the text context, just send None or Send a string message
                #     settings.DEFAULT_FROM_EMAIL,
                #     [user.email],
                # )
                # msg.attach_alternative(convert_to_html_content, "text/html")
                # msg.send(fail_silently=False)'''

            ''' # subject = 'Verify Your Email Address'
            # uid = urlsafe_base64_encode(force_bytes(user.pk))
            # token = default_token_generator.make_token(user)
            # verify_url = reverse('api:verify-email') + f'?uid={uid}&token={token}'
            # reset_link = f"http://localhost:8000{verify_url}"
            # message = f'Hi {user.first_name},\n\nPlease verify your email address by clicking the following link:\n\n{reset_link}'
            # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            # return Response({'message': 'Verification email resent successfully.'}, status=status.HTTP_200_OK)'''
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

