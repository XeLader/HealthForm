from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from ..forms import MedicineCreateForm
from ..models.medicine import Medicine

@login_required
def medicine_create(request):
    if request.method == "POST":
        form = MedicineCreateForm(request.POST)
        if form.is_valid():
            med = form.save()
            messages.success(request, f"Препарат «{med.title}» добавлен.")
            return redirect("handbook") 
    else:
        form = MedicineCreateForm()

    return render(request, "medicines/medicine_form.html", {"form": form, "nav_section": "handbook"})
    

@login_required()
def medicine_edit(request, pk):
    med = get_object_or_404(Medicine, pk=pk)
    if request.method == "POST":
        form = MedicineCreateForm(request.POST, instance=med)
        if form.is_valid():
            med = form.save()
            messages.success(request, f"Препарат «{med.title}» изменён.")
            return redirect("handbook") 
    else:
        form = MedicineCreateForm(instance=med)
    return render(request, "medicines/medicine_form.html", {"form": form, "med": med, "nav_section": "handbook"})
