import factory
from faker import Factory as FakerFactory

from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from apps.enquiries.models import Enquiry
from apps.profiles.models import Profile

User = get_user_model()
faker = FakerFactory.create()


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory('tests.factories.UserFactory')
    phone_number = factory.LazyAttribute(function=lambda x: faker.phone_number()[:13])
    about_me = factory.LazyAttribute(function=lambda x: faker.sentence(nb_words=5))
    licence = factory.LazyAttribute(function=lambda x: faker.text(max_nb_chars=6))
    photo = factory.LazyAttribute(function=lambda x: faker.file_extension(category='image'))
    gender = factory.LazyAttribute(function=lambda x: f'other')
    country = factory.LazyAttribute(function=lambda x: faker.country_code())
    city = factory.LazyAttribute(function=lambda x: faker.city())
    is_buyer = False
    is_seller = False
    is_agent = False
    top_agent = False
    rating = factory.LazyAttribute(function=lambda x: faker.random_int(min=1, max=5))
    reviews = factory.LazyAttribute(function=lambda x: faker.random_int(min=0, max=25))

    class Meta:
        model = Profile


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.LazyAttribute(function=lambda x: faker.first_name())
    first_name = factory.LazyAttribute(function=lambda x: faker.first_name())
    last_name = factory.LazyAttribute(function=lambda x: faker.last_name())
    email = factory.LazyAttribute(function=lambda x: f'alpha@gmail.com')
    password = factory.LazyAttribute(function=lambda x: faker.password())
    is_staff = False
    is_active = False

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)

        if 'is_superuser' in kwargs:
            return manager.create_superuser(*args, **kwargs)
        return manager.create_user(*args, **kwargs)


class EnquiryFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(function=lambda x: faker.first_name())
    phone_number = factory.LazyAttribute(function=lambda x: faker.phone_number()[:13])
    email = factory.LazyAttribute(function=lambda x: f'alpha@gmail.com')
    subject = factory.LazyAttribute(function=lambda x: faker.sentence(nb_words=5))
    message = factory.LazyAttribute(function=lambda x: faker.text())

    class Meta:
        model = Enquiry
