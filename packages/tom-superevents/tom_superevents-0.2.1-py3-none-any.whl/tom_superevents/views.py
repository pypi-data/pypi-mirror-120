from django.views.generic import DetailView, ListView
from rest_framework import viewsets
from rest_framework import permissions

from tom_superevents.superevent_clients.gravitational_wave import GravitationalWaveClient
from .models import EventCandidate, EventLocalization, Superevent
from .serializers import EventCandidateSerializer, EventLocalizationSerializer, SupereventSerializer


class SupereventListView(ListView):
    model = Superevent
    template_name = 'tom_superevents/index.html'


class SupereventDetailView(DetailView):
    model = Superevent
    template_name = 'tom_superevents/detail.html'

    # TODO: consider combining these dictionaries
    template_mapping = {
        Superevent.SupereventType.GRAVITATIONAL_WAVE: 'tom_superevents/superevent_detail/gravitational_wave.html',
        Superevent.SupereventType.GAMMA_RAY_BURST: 'tom_superevents/superevent_detail/gamma_ray_burst.html',
        Superevent.SupereventType.NEUTRINO: 'tom_superevents/superevent_detail/neutrino.html',
    }
    client_mapping = {
        Superevent.SupereventType.GRAVITATIONAL_WAVE: GravitationalWaveClient(),
        Superevent.SupereventType.GAMMA_RAY_BURST: None,
        Superevent.SupereventType.NEUTRINO: None,
        Superevent.SupereventType.UNKNOWN: None,
    }

    def get_template_names(self):
        obj = self.get_object()
        return [self.template_mapping[obj.superevent_type]]

    # TODO: error handling
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        superevent_client = self.client_mapping[obj.superevent_type]
        # TODO: should define superevent_client API (via ABC) for clients to implement
        if superevent_client is not None:
            context['superevent_data'] = superevent_client.get_superevent_data(obj.superevent_id)
            context.update(superevent_client.get_additional_context_data(obj.superevent_id))
        return context


# Django Rest Framework Views


class SupereventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Superevents to be viewed or edited.
    """
    queryset = Superevent.objects.all()
    serializer_class = SupereventSerializer
    permission_classes = []


class EventCandidateViewSet(viewsets.ModelViewSet):
    queryset = EventCandidate.objects.all()
    serializer_class = EventCandidateSerializer
    permission_classes = []  # TODO: re-implement auth permissions

    def get_serializer(self, *args, **kwargs):
        # In order to ensure the list_serializer_class is used for bulk_create, we check that the POST data is a list
        # and add `many = True` to the kwargs
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True

        return super().get_serializer(*args, **kwargs)


class EventLocalizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows EventLocalizations to be viewed or edited.
    """
    queryset = EventLocalization.objects.all()
    serializer_class = EventLocalizationSerializer
    permission_classes = [permissions.IsAuthenticated]
