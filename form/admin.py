from django.contrib import admin
from .models import Report
from .models import Patient
from .models import Biochemistry
from .models import Medicine
from .models import Prescription

# Register your models here.

admin.site.register(Report)
admin.site.register(Patient)
admin.site.register(Biochemistry)
admin.site.register(Medicine)
admin.site.register(Prescription)
