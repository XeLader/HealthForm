from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Report, Biochemistry
from .forms import ReportForm 

# Create your views here.

def report_list(request):
    forms = Report.objects.order_by('created_date')
    return render(request, 'form/report_list.html',{'forms':forms})


def report_detail(request, pk):
	report = get_object_or_404(Report, pk = pk)
	biochems = Biochemistry.objects.filter(patient = report.patient)
	return render(request, 'form/report_detail.html', {'report':report, 'biochems':biochems})

def report_new(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('report_detail', pk=post.pk)
    else:
        form = ReportForm()
    return render(request, 'form/report_edit.html', {'form': form})


def report_edit(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        form = ReportForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('report_detail', pk=post.pk)
    else:
        form = ReportForm(instance=post)
    return render(request, 'form/report_edit.html', {'form': form})
