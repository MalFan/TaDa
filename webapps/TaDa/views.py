from django.shortcuts import render

# Create your views here.
def admin_homepage(request):
	context = {}
	return render(request, 'admin_homepage.html', context)

def admin_search(request):
	context = {}
	return render(request, 'admin_homepage.html', context)