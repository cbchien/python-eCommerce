from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
from billings.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart

# import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY","sk_test_iiOy8vTuT7N0fg7GQZ0NLxxD")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_PMqhLzcmfBpbJ7IYW61DcdSF")
# stripe.api_key = STRIPE_SECRET_KEY

def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        "id": product.id,
        "url": product.get_absolute_url(),
        "name": product.name,
        "price": product.price
        } 
        for product in cart_obj.products.all()]
    cart_data = {
        "products": products,
        "subtotal":cart_obj.subtotal,
        "total": cart_obj.total
        }
    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})

def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print('Check product again.')
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
            print("Removing", product_obj.title)
        else:
            cart_obj.products.add(product_obj)
            added = True
            print("Adding", product_obj.title)
        request.session['cart_item_count'] = cart_obj.products.count()
        if request.is_ajax():
            print("Ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count()
            }
            print(json_data)
            return JsonResponse(json_data, status=200)
    return redirect("cart:home")

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    has_card = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()

    # Associate billing and shipping addresses
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
            # shipping_address_qs = address_qs.filter(address_type="shipping")
            # billing_address_qs = address_qs.filter(address_type="billing")

        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        has_card = billing_profile.has_card
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if  billing_address_id or shipping_address_id:
            order_obj.save()
        

    # Process to check required information and complete checkout
    if request.method == "POST":
        is_done = order_obj.check_done()
        if is_done:
            did_charge, charge_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_item_count'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                return redirect("cart:success")
            else:
                print(charge_msg)
                return redirect("cart:checkout")
                
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
    }
    return render(request, "carts/checkout.html", context)

def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})