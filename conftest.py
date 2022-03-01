import pytest

from pytest_factoryboy import register

from tests.factories import (UserFactory,
                             ProfileFactory,
                             EnquiryFactory)

register(factory_class=UserFactory)
register(factory_class=ProfileFactory)
register(factory_class=EnquiryFactory)


@pytest.fixture
def base_user(db, user_factory):
    return user_factory.create()


@pytest.fixture
def superuser(db, user_factory):
    return user_factory.create(is_staff=True, is_superuser=True)


@pytest.fixture
def profile(db, profile_factory):
    return profile_factory.create()


@pytest.fixture
def enquiry(db, enquiry_factory):
    return enquiry_factory.create()
