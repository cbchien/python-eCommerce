from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import stripe
from django.utils.http import is_safe_url

from .models import BillingProfile
stripe.api_key = "sk_test_iiOy8vTuT7N0fg7GQZ0NLxxD"
STRIPE_PUB_KEY = "pk_test_PMqhLzcmfBpbJ7IYW61DcdSF"

def payment_method_view(request):
    # if request.user.is_authenticated():
    #     billing_profile = request.user.billingprofile
    #     my_customer_id = billing_profile.customer_id
    
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/cart")

    next_url = None
    next_ = request.GET.get("next")
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})

def payment_method_create_view(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Connot find this user"}, status=401)
        token = request.POST.get('token')
        if token is not None:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            card_response = customer.sources.create(source=token)
            print(card_response)
        return JsonResponse({"message": "Success! Your card was added"})
    return HttpResponse("error", status=401)