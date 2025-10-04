from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reports/', views.report_list, name='report_list'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
    path('report/new/', views.report_new, name='report_new'),
    path('report/<int:pk>/edit/', views.report_edit, name='report_edit'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
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
]
