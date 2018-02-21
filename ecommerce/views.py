from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model

from .forms import ContactForm, LoginForm, RegisterForm

# def home_page(request):
# 	return HttpResponse(html_)

def home_page(request):
	context = {
		"title":"Hello World! Yeah, Context!",
		"content":"This is the home page",
	}
	if request.user.is_authenticated():
		context["premium_content"] = "This is exclusive content"
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
		"title":"Hello Contact Page!",
		"content":"This is the contact page.",
		"form":contact_form
	}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
	# if request.method == "POST":
	# 	print(request.POST)
	# 	print('Name is', request.POST.get('fullname'))
	# 	print('Email is', request.POST.get('email'))
	# 	print('Message is', request.POST.get('message'))
	return render(request, "contact/view.html", context)

def login_page(request):
	form = LoginForm(request.POST or None)
	context = {
		"form":form
	}
	print("User logged in?", request.user.is_authenticated())
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			# context['form'] = LoginForm()
			return redirect("/")
			print("User logged in?", request.user.is_authenticated(), 'username', username)
		else:
			print("Not logged in")

	return render(request, "auth/login.html", context)


User = get_user_model()
def register_page(request):
	form = RegisterForm(request.POST or None)
	context = {
		"form":form
	}
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		new_user = User.objects.create_user(username, email, password)
		print(new_user)
	return render(request, "auth/register.html", context)