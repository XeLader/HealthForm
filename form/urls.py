from django.urls import path
from .views.labs import *
from .views.medicine import *
from .views.patients import *
from .views.reports import *
from .views.views import *
from .views.survey import (
    CreateSurveyInviteView,
    PublicSurveySectionView,
    PublicSurveyFinishView,
    SurveyResultsView)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('reports/', report_list, name='report_list'),
    path('report/<int:pk>/', report_detail, name='report_detail'),
    path('report/new/', report_new, name='report_new'),
    path('report/<int:pk>/edit/', report_edit, name='report_edit'),
    path('report/<int:pk>/print/', report_print_config, name='report_print_config'),
    path('report/<int:pk>/print/preview/', report_print_preview, name='report_print_preview'),
    path('patient/<int:pk>/', patient_detail, name='patient_detail'),
    path('patient/<int:pk>/report/new', report_new_for_patient, name='report_new_for_patient'),
    path('patient/<int:pk>/edit', patient_edit, name='patient_edit'),
    path('patients', patient_list, name='patient_list'),
    path('patient/new/', patient_new, name='patient_new'),
    path('patient/<int:pk>/prescription/new', prescription_new, name='prescription_new'),
    path('patient/<int:pk>/biochemistry/new', biochemistry_new, name='biochemistry_new'),
    path('patient/<int:pk>/proteinmetabolism/new', proteinmetabolism_new, name='proteinmetabolism_new'),
    path('patient/<int:pk>/lipidmetabolism/new', lipidmetabolism_new, name='lipidmetabolism_new'),
    path('patient/<int:pk>/carbohydratemetabolism/new', carbohydratemetabolism_new, name='carbohydratemetabolism_new'),
    path('patient/<int:pk>/ironmetabolism/new', ironmetabolism_new, name='ironmetabolism_new'),
    path('patient/<int:pk>/micronutrients/new', micronutrients_new, name='micronutrients_new'),
    path('patient/<int:pk>/inflammatorymarkers/new', inflammatorymarkers_new, name='inflammatorymarkers_new'),
    path('patient/<int:pk>/allergiesinfections/new', allergiesinfections_new, name='allergiesinfections_new'),
    path('patient/<int:pk>/thyroidfunction/new', thyroidfunction_new, name='thyroidfunction_new'),
    path('patient/<int:pk>/hematology/new', hematology_new, name='hematology_new'),
    path('patient/<int:pk>/platelets/new', platelets_new, name='platelets_new'),
    path('patient/<int:pk>/leukocytes/new', leukocytes_new, name='leukocytes_new'),
    path('patient/<int:pk>/hormonallevels/new', hormonallevels_new, name='hormonallevels_new'),
    path('patient/<int:pk>/labs/upload/', labdoc_upload, name='labdoc_upload'),
    path('patient/<int:pk>/labs/files/', patient_labdocs, name='patient_labdocs'),
    path('labdoc/<uuid:doc_id>/', labdoc_fill, name='labdoc_fill'),
    path('labdoc/<uuid:doc_id>/done/', labdoc_mark_done, name='labdoc_mark_done'),
    path('labdoc/<uuid:doc_id>/add/<slug:kind>/', labdoc_add_lab, name='labdoc_add_lab'),
    path('labdoc/<uuid:doc_id>/unlink/<int:entry_id>/', labdoc_unlink_entry, name='labdoc_unlink_entry'),
    path('labdoc/<uuid:doc_id>/file/', labdoc_file, name='labdoc_file'),
    
    path('patient/<int:pk>/questionnaires/new/', CreateSurveyInviteView.as_view(), name='survey_invite_create'),
    path('q/<uuid:token>/', PublicSurveySectionView.as_view(), name='survey_run_public'),
    path('q/<uuid:token>/finish/', PublicSurveyFinishView.as_view(), name='survey_finish_public'),
    
    path('patient/<int:pk>/questionnaires/<uuid:token>/results/', SurveyResultsView.as_view(), name='survey_results'),
    path('invites/new/', invite_new, name='invite_new'),
    path('invite/<uuid:token>/', accept_invite, name='accept_invite'),
    
    path('labdoc/<uuid:doc_id>/file/', labdoc_file, name='labdoc_file'),
    path('labs/entry/<int:pk>/', labentry_detail, name='labentry_detail'),
    
    path("medicines/new/", medicine_create, name="medicine_create"),
    path("medicines/<int:pk>/edit", medicine_edit, name="medicine_edit"),
    path("medicines/<int:pk>/usage/", medicine_usage, name="medicine_usage"),

    
    path("handbook/", handbook, name="handbook"),

    path("patient/<int:patient_pk>/diagnosis/new/", DiagnosticHypothesisCreateView.as_view(), name="diagnosis_create",),
    path("diagnosis/<int:pk>/edit/",DiagnosticHypothesisUpdateView.as_view(),name="diagnosis_edit"),
]

