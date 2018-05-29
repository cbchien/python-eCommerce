from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model

from .forms import ContactForm

# def home_page(request):
# 	return HttpResponse(html_)

def home_page(request):
	context = {
		"title":"Welcome to CBCommerce",
		"content":"This is a ecommerce demo page",
	}
	try:
		if request.user.is_authenticated():
			context["premium_content"] = "You are now logged in to our website"
	except:
		pass
	return render(request, "home_page.html", context)

def about_page(request):
	context = {
		"title":"Hello About Page!",
		"content":"This is the about page"
	}
	return render(request, "home_page.html", context)

def contact_page(request):
	contact_form = ContactForm(request.POST or None)
	context = {
		"title": "Hello Contact Page!",
		"content": "This is the contact page.",
		"form": contact_form,
	}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
		if request.is_ajax():
			return JsonResponse({"message": "Thank You"})
	if contact_form.errors:
		errors = contact_form.errors.as_json()
		if request.is_ajax():
			return HttpResponse(errors, status=400, content_type='application/json')
	# if request.method == "POST":
	# 	print(request.POST)
	# 	print('Name is', request.POST.get('fullname'))
	# 	print('Email is', request.POST.get('email'))
	# 	print('Message is', request.POST.get('message'))
	return render(request, "contact/view.html", context)