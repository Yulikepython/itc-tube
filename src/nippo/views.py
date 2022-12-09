from django.shortcuts import render

def nippoListView(request):
	return render(request, "nippo/nippo-list.html")
