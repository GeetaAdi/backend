from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from djangocrud.api import views
from rest_framework.authtoken.views import ObtainAuthToken

router = routers.DefaultRouter()
router.register(r'attitude', views.AttitudeViewSet)
router.register(r'empathy', views.EmpathyViewSet)
router.register(r'policy', views.PolicyViewSet)
router.register(r'professionalism', views.ProfessionalismViewSet)
router.register(r'teaching', views.TeachingViewSet)
router.register(r'responses', views.ResponsesViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djangocrud.api.urls')),
    # path('', include(router.urls)),
]
