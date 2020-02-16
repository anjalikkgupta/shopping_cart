from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Cart, Order



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'products/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'products/login.html', {})


def logout_request(request):
    logout(request)
    return render(request, 'products/logout.html', {})


def product_list(request):
    product = Product.objects.all()
    user = request.user
    # orders = Order.objects.filter(user=user, ordered=False)
    # order = orders[0]
    # if orders.exists():
    #     order_count = order.orderitems.count()
    # else:
    #     order_count = None, 0
    return render(request,'products/home.html', {'product': product})



def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = Cart.objects.get_or_create(
        item=item,
        user=request.user
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect("home")
        else:
            order.orderitems.add(order_item)
            return redirect("home")
    else:
        order = Order.objects.create(
            user=request.user)
        order.orderitems.add(order_item)
        return redirect("home")


@login_required
def increasecart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = Cart.objects.get_or_create(
        item=item,
        user=request.user
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect("cart_items")
        else:
            order.orderitems.add(order_item)
            return redirect("cart_items")
    else:
        order = Order.objects.create(
            user=request.user)
        order.orderitems.add(order_item)
        return redirect("cart_items")


# def remove_from_cart(request, slug):
#     item = get_object_or_404(Product, slug=slug)
#     cart_qs = Cart.objects.filter(user=request.user, item=item)
#     if cart_qs.exists():
#         cart = cart_qs[0]
#         # Checking the cart quantity
#         if cart.quantity > 1:
#             cart.quantity -= 1
#             cart.save()
#         else:
#             cart_qs.delete()
#     order_qs = Order.objects.filter(
#         user=request.user,
#         ordered=False
#     )
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.orderitems.filter(item__slug=item.slug).exists():
#             order_item = Cart.objects.filter(
#                 item=item,
#                 user=request.user,
#             )[0]
#             order.orderitems.remove(order_item)
#             messages.info(request, "This item was removed from your cart.")
#             return redirect("mainapp:home")
#         else:
#             messages.info(request, "This item was not in your cart")
#             return redirect("mainapp:home")
#     else:
#         messages.info(request, "You do not have an active order")
#         return redirect("core:home")


@login_required
def cartview(request):
    user = request.user
    carts = Cart.objects.filter(user=user)
    orders = Order.objects.filter(user=user, ordered=False)

    if carts.exists():
        order = orders[0]
        return render(request, 'products/product_list.html', {"carts": carts, 'order': order})
    else:
        return redirect("home")


@login_required
def decreasecart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
            messages.info(request, f"{item.title} quantity has updated.")
            return redirect("cart_items")
        else:
            messages.info(request, f"{item.title} quantity has updated.")
            return redirect("cart_items")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart_items")


# def checkoutview(request):
#     # Checkout view
#     form = BillingForm
#
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     order_items = order_qs[0].orderitems.count()
#     order_total = order_qs[0].get_totals()
#     # context = {"form": form, "order_items": order_items, "order_total": order_total}
#     # Getting the saved saved_address
#     saved_address = BillingAddress.objects.filter(user=request.user)
#     if saved_address.exists():
#         savedAddress = saved_address.first()
#         # context = {"form": form, "order_items": order_items, "order_total": order_total, "savedAddress": savedAddress}
#     if request.method == "POST":
#         saved_address = BillingAddress.objects.filter(user=request.user)
#         if saved_address.exists():
#
#             savedAddress = saved_address.first()
#             form = BillingForm(request.POST, instance=savedAddress)
#             if form.is_valid():
#                 billingaddress = form.save(commit=False)
#                 billingaddress.user = request.user
#                 billingaddress.save()
#         else:
#             form = BillingForm(request.POST)
#             if form.is_valid():
#                 billingaddress = form.save(commit=False)
#                 billingaddress.user = request.user
#                 billingaddress.save()
#
#     return render(request, 'products/newindex.html', {"form": form, "order_items": order_items, "order_total": order_total, "savedAddress": savedAddress})