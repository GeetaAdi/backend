from django.urls import include, path
from rest_framework import routers
from djangocrud.api import views
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings

from knox.views import LogoutView

from .views import UserAPIView, RegisterAPIView, LoginAPIView, scores, email

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'attitude', views.AttitudeViewSet)
router.register(r'empathy', views.EmpathyViewSet)
router.register(r'policy', views.PolicyViewSet)
router.register(r'professionalism', views.ProfessionalismViewSet)
router.register(r'teaching', views.TeachingViewSet)
router.register(r'responses', views.ResponsesViewSet)
router.register(r'preSurvey', views.PreSurveyViewSet)
router.register(r'postSurvey', views.PostSurveyViewSet)
router.register(r'finalFeedback', views.FinalFeedbackViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'cpcq', views.CpcqViewSet)
router.register(r'presurvey_questions', views.PreSurveyQuestionsViewSet)
router.register(r'postsurvey_questions', views.PostSurveyQuestionsViewSet)
router.register(r'status', views.StatusViewSet)



urlpatterns = [
    path('', include('knox.urls')),
    path('scores/', scores ),
    path('email/', email ),
    path('user', UserAPIView.as_view()),
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('logout', LogoutView.as_view(), name='knox_logout'),
    path('responses_all/', views.ResponsesAllView.as_view()),
    path('cpcq_response/', views.CPCQResponsesView.as_view()),
    path('graphs/', views.ReportsView.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)