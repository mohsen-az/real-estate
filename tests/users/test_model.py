import pytest

from django.contrib.auth.models import BaseUserManager


def test_base_user_representation(base_user):
    assert base_user.__str__() == base_user.username


def test_base_user_full_name(base_user):
    full_name = f'{base_user.first_name} {base_user.last_name}'
    assert base_user.get_full_name == full_name


def test_base_user_short_name(base_user):
    short_name = base_user.username
    assert base_user.get_short_name() == short_name


def test_base_user_normalize_email(base_user):
    email = '     alPHa@Gmail.Com         '
    assert base_user.email == BaseUserManager.normalize_email(email).lower()


def test_superuser_normalize_email(superuser):
    email = '     alPHa@Gmail.Com         '
    assert superuser.email == BaseUserManager.normalize_email(email).lower()


def test_superuser_is_not_staff(user_factory):
    with pytest.raises(expected_exception=ValueError) as error:
        user_factory.create(is_superuser=True, is_staff=False)
    assert str(error.value) == 'Superusers must have is_staff=True'


def test_superuser_is_not_superuser(user_factory):
    with pytest.raises(expected_exception=ValueError) as error:
        user_factory.create(is_superuser=False, is_staff=True)
    assert str(error.value) == 'Superusers must have is_superuser=True'


def test_base_user_with_not_email(user_factory):
    with pytest.raises(expected_exception=ValueError) as error:
        user_factory.create(email=None)
    assert str(error.value) == 'Base User Account: An email address is required.'


def test_base_user_with_not_username(user_factory):
    with pytest.raises(expected_exception=ValueError) as error:
        user_factory.create(username=None)
    assert str(error.value) == 'Users must submit username.'


def test_base_user_with_not_first_name(user_factory):
    with pytest.raises(expected_exception=ValueError) as error:
        user_factory.create(first_name=None)
    assert str(error.value) == 'Users must submit firstname.'


def test_base_user_with_not_last_name(user_factory):
    with pytest.raises(expected_exception=ValueError) as error:
        user_factory.create(last_name=None)
    assert str(error.value) == 'Users must submit lastname.'


def test_superuser_with_not_email(user_factory):
    with pytest.raises(expected_exception=ValueError) as error:
        user_factory.create(email=None, is_staff=True, is_superuser=True)
    assert str(error.value) == 'Admin User Account: An email address is required.'


def test_superuser_with_not_password(user_factory):
    with pytest.raises(expected_exception=ValueError) as error:
        user_factory.create(is_staff=True, is_superuser=True, password=None)
    assert str(error.value) == 'Superuser must have a password'


def test_base_user_with_incorrect_email(user_factory):
    with pytest.raises(expected_exception=ValueError) as error:
        user_factory.create(email='abc.com')
    assert str(error.value) == 'You must provide a valid email address.'
