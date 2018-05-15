from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.http import is_safe_url

from .models import GuestEmail
from .forms import LoginForm, RegisterForm, GuestForm
from .signals import user_logged_in_signal

def guest_register_page(request):
	form = GuestForm(request.POST or None)
	context = {
		"form":form
	}
	next_ = request.GET.get("next")
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None

	if form.is_valid():
		email = form.cleaned_data.get("email")
		new_guest_email = GuestEmail.objects.create(email=email)
		request.session['guest_email_id'] = new_guest_email.id
		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)
		else:
			return redirect("/register/")
	return redirect("/register/")

class LoginView(FormView):
	form_class = LoginForm
	success_url = "/"
	template_name = "accounts/login.html"

	def form_valid(self, form):
		request = self.request
		next_ = request.GET.get("next")
		next_post = request.POST.get('next')
		redirect_path = next_ or next_post or None

		email	 = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		user = authenticate(request, username=email, password=password)
		if user is not None:
			login(request, user)
			user_logged_in_signal.send(user.__class__, instance=user, request=request)
			try:
				del request.session['guest_email_id']
			except:
				pass
				
			if is_safe_url(redirect_path, request.get_host()):
			    return redirect(redirect_path)
			else:
			    return redirect("/")
			print("User logged in?", request.user.is_authenticated(), 'username', username)
		return super(LoginView, self).form_invalid(form)

# def login_page(request):
# 	form = LoginForm(request.POST or None)
# 	context = {
# 		"form":form
# 	}
# 	print("User logged in?", request.user.is_authenticated())
# 	next_ = request.GET.get("next")
# 	next_post = request.POST.get('next')
# 	redirect_path = next_ or next_post or None

# 	if form.is_valid():
# 		print(form.cleaned_data)
# 		username = form.cleaned_data.get("username")
# 		password = form.cleaned_data.get("password")
# 		user = authenticate(request, username=username, password=password)
# 		if user is not None:
# 			login(request, user)
# 			try:
# 				del request.session['guest_email_id']
# 			except:
# 				pass
# 			# context['form'] = LoginForm()
# 			if is_safe_url(redirect_path, request.get_host()):
# 			    return redirect(redirect_path)
# 			else:
# 			    return redirect("/")
# 			print("User logged in?", request.user.is_authenticated(), 'username', username)
# 		else:
# 			print("Not logged in")

# 	return render(request, "accounts/login.html", context)

def logout_page(request):
	logout(request)
	context = {
		"title": "Thank you for visiting",
		"content": "You have successfully logged out.",
	}
	return render(request, "accounts/logout.html", context)

class RegisterView(CreateView):
	form_class = RegisterForm
	template_name = "accounts/register.html"
	success_url = "/login/"

User = get_user_model()
def register_page(request):
	form = RegisterForm(request.POST or None)
	context = {
		"form": form
	}
	if form.is_valid():
		form.save()
		# username = form.cleaned_data.get("username")
		# email = form.cleaned_data.get("email")
		# password = form.cleaned_data.get("password")
		# new_user = User.objects.create_user(username, email, password)
	return render(request, "accounts/register.html", context)