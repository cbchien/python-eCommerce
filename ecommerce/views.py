from django.http import HttpResponse
from django.shortcuts import render

from .forms import ContactForm

# def home_page(request):
# 	return HttpResponse(html_)

def home_page(request):
	context = {
		"title":"Hello World! Yeah, Context!",
		"content":"This is the home page"
	}
	return render(request, "home_page.html", context)

def about_page(request):
	context = {
		"title":"Hello About Page!",
		"content":"This is the about page"
	}
	return render(request, "home_page.html", context)

def contact_page(request):
	contact_form = ContactForm()
	context = {
		"title":"Hello Contact Page!",
		"content":"This is the contact page.",
		"form":contact_form
	}
	if request.method == "POST":
		print(request.POST)
		print('Name is', request.POST.get('fullname'))
		print('Email is', request.POST.get('email'))
		print('Message is', request.POST.get('message'))
	return render(request, "contact/view.html", context)
