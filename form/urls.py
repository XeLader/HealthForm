from django.urls import path
from . import views
from .views import (
    CreateSurveyInviteView,   # создаёт токен на карточке пациента (для врача/сотрудника)
    PublicSurveySectionView,  # публичный мастер по токену
    PublicSurveyFinishView,
    SurveyResultsView,
)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reports/', views.report_list, name='report_list'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
    path('report/new/', views.report_new, name='report_new'),
    path('report/<int:pk>/edit/', views.report_edit, name='report_edit'),
    path('report/<int:pk>/print/', views.report_print_config, name='report_print_config'),
    path("report/<int:pk>/print/preview/", views.report_print_preview, name="report_print_preview"),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patient/<int:pk>/report/new', views.report_new_for_patient, name='report_new_for_patient'),
    path('patient/<int:pk>/edit', views.patient_edit, name='patient_edit'),
    path('patients', views.patient_list, name='patient_list'),
    path('patient/new/', views.patient_new, name='patient_new'),
    path('patient/<int:pk>/prescription/new', views.prescription_new, name='prescription_new'),
    path('patient/<int:pk>/biochemistry/new', views.biochemistry_new, name='biochemistry_new'),
    path('patient/<int:pk>/proteinmetabolism/new', views.proteinmetabolism_new, name='proteinmetabolism_new'),
    path('patient/<int:pk>/lipidmetabolism/new', views.lipidmetabolism_new, name='lipidmetabolism_new'),
    path('patient/<int:pk>/carbohydratemetabolism/new', views.carbohydratemetabolism_new, name='carbohydratemetabolism_new'),
    path('patient/<int:pk>/ironmetabolism/new', views.ironmetabolism_new, name='ironmetabolism_new'),
    path('patient/<int:pk>/micronutrients/new', views.micronutrients_new, name='micronutrients_new'),
    path('patient/<int:pk>/inflammatorymarkers/new', views.inflammatorymarkers_new, name='inflammatorymarkers_new'),
    path('patient/<int:pk>/allergiesinfections/new', views.allergiesinfections_new, name='allergiesinfections_new'),
    path('patient/<int:pk>/thyroidfunction/new', views.thyroidfunction_new, name='thyroidfunction_new'),
    path('patient/<int:pk>/hematology/new', views.hematology_new, name='hematology_new'),
    path('patient/<int:pk>/platelets/new', views.platelets_new, name='platelets_new'),
    path('patient/<int:pk>/leukocytes/new', views.leukocytes_new, name='leukocytes_new'),
    path('patient/<int:pk>/hormonallevels/new', views.hormonallevels_new, name='hormonallevels_new'),
    
    path("patient/<int:pk>/questionnaires/new/", CreateSurveyInviteView.as_view(), name="survey_invite_create"),
    path("q/<uuid:token>/", PublicSurveySectionView.as_view(), name="survey_run_public"),
    path("q/<uuid:token>/finish/", PublicSurveyFinishView.as_view(), name="survey_finish_public"),
    
    path("patient/<int:pk>/questionnaires/<uuid:token>/results/", SurveyResultsView.as_view(), name="survey_results"),
    path("invites/new/", views.invite_new, name="invite_new"),
    path("invite/<uuid:token>/", views.accept_invite, name="accept_invite"),
]

