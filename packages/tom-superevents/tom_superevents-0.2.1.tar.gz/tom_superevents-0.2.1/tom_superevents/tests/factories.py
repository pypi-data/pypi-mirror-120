import factory

from tom_superevents.models import Superevent, EventLocalization


class SupereventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Superevent

    superevent_id = factory.Faker('pystr')
    superevent_url = factory.Faker('pystr')


class EventLocalizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EventLocalization
