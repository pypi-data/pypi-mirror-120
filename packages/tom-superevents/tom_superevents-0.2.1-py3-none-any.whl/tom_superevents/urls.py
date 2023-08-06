from django.urls import path

from tom_common.api_router import SharedAPIRootRouter

from . import views

router = SharedAPIRootRouter()
router.register(r'superevents', views.SupereventViewSet)
router.register(r'eventlocalizations', views.EventLocalizationViewSet)
router.register(r'eventcandidates', views.EventCandidateViewSet)

# app_name provides namespace in {% url %} template tag
# (i.e. {% url 'superevents:detail' <pk> %}
app_name = 'superevents'

urlpatterns = [
    path('', views.SupereventListView.as_view(), name='index'),
    path('<int:pk>/', views.SupereventDetailView.as_view(), name='detail'),
]
