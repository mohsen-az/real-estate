from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address."))

    def create_user(
        self, username, first_name, last_name, email, password=None, **kwargs
    ):
        if not username:
            raise ValueError(_("Users must submit username."))

        if not first_name:
            raise ValueError(_("Users must submit firstname."))

        if not last_name:
            raise ValueError(_("Users must submit lastname."))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Base User Account: An email address is required."))

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            **kwargs
        )

        user.set_password(password)
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, first_name, last_name, email, password=None, **kwargs
    ):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if not kwargs.get("is_staff"):
            raise ValueError(_("Superusers must have is_staff=True"))

        if not kwargs.get("is_superuser"):
            raise ValueError(_("Superusers must have is_superuser=True"))

        if not password:
            raise ValueError(_("Superuser must have a password"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Admin User Account: An email address is required."))

        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **kwargs
        )
        user.save(using=self._db)
        return user
