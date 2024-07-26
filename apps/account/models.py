from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext as _
from common.models.base_models import Base_model
from common.validators import validate_image_extension,validate_max_file_size
from .utils import profile_image_storage

class UserManager(BaseUserManager):
    def create_user(
        self, email, first_name=None, last_name=None, password=None, **extra_fields
    ):
        if not email:
            raise ValueError(_("The Email field must be set"))
        if not first_name:
            raise ValueError(_("The First Name field must be set"))
        if not last_name:
            raise ValueError(_("The Last Name field must be set"))

        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name=None, last_name=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)


class User(AbstractUser, Base_model):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    is_verify = models.BooleanField(default=False)
    phone = models.CharField(max_length=100)
    avatar = models.FileField(
        upload_to=profile_image_storage,
        validators=[validate_image_extension, validate_max_file_size],
        blank=True,
        null=True,
    )
    
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
