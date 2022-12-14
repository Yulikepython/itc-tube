from django.shortcuts import render
from .models import NippoModel
from .forms import  NippoFormClass

def nippoListView(request):
    template_name = "nippo/nippo-list.html"
    ctx = {}
    qs = NippoModel.objects.all()
    ctx["object_list"] = qs
    return render(request, template_name, ctx)

def nippoDetailView(request, pk):
    template_name = "nippo/nippo-detail.html"
    ctx = {}
    q = NippoModel.objects.get(pk=pk)
    ctx["object"] = q
    return render(request, template_name, ctx)

def nippoCreateView(request):
    template_name = "nippo/nippo-form.html"
    form = NippoFormClass(request.POST or None)
    ctx = {}
    ctx["form"] = form
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj = NippoModel(title=title, content=content)
        obj.save()
    return render(request, template_name, ctx)

def nippoUpdateFormView(request, pk):
    template_name = "nippo/nippo-form.html"
    obj = NippoModel.objects.get(pk=pk)
    initial_values = {"title": obj.title, "content":obj.content}
    form = NippoFormClass(request.POST or initial_values)
    ctx = {"form": form}
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj.title = title
        obj.content = content
        obj.save()
    return render(request, template_name, ctx)
