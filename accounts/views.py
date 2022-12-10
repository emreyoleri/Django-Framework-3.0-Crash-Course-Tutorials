from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.contrib import messages

from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter


@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            user = form.save()

            username = form.cleaned_data.get("username")

            group = Group.objects.get(name="customer")

            user.groups.add(group)

            Customer.objects.create(
                user=user, name=user.username, email=user.email)

            messages.success(
                request, "Account was created for " + username)

            return redirect("login")

    context = {"form": form}

    return render(request, "accounts/register.html", context)


@unauthenticated_user
def loginPage(request):

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            return redirect("home")

        else:

            messages.info(request, "username OR password is incorrect")

    context = {}

    return render(request, "accounts/login.html", context)


def logoutUser(request):

    logout(request)

    return redirect("login")


# @allowed_users(allowed_roles=["admin"])
@login_required(login_url="login")
@admin_only
def home(request):
    orders = Order.objects.all()

    customers = Customer.objects.all()

    total_orders = orders.count()

    total_customers = customers.count()

    delivered = orders.filter(status="Delivered").count()

    pending = orders.filter(status="Pending").count()

    context = {
        "orders": orders,
        "customers": customers,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "delivered": delivered,
        "pending": pending
    }

    return render(request, "accounts/dashboard.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def userPage(request):

    orders = request.user.customer.order_set.all()

    total_orders = orders.count()

    delivered = orders.filter(status="Delivered").count()

    pending = orders.filter(status="Pending").count()

    context = {
        "orders": orders,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending
    }

    return render(request, "accounts/user.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def accountSettings(request):

    customer = request.user.customer

    form = CustomerForm(instance=customer)

    if request.method == "POST":

        form = CustomerForm(request.POST, request.FILES, instance=customer)

        if form.is_valid():

            form.save()

            if not customer.profile_pic:

                customer.profile_pic = "user-logo1.jpg"

                customer.save()

    context = {"form": form}

    return render(request, "accounts/account_settings.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def products(request):

    products = Product.objects.all()

    context = {"products": products}

    return render(request, "accounts/products.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def customer(request, pk):

    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()

    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)

    orders = myFilter.qs

    context = {
        "customer": customer,
        "orders": orders,
        "total_orders": total_orders,
        "myFilter": myFilter
    }

    return render(request, "accounts/customer.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def createOrder(request, pk):

    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=("product", "status"), extra=3)

    customer = Customer.objects.get(id=pk)

    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == "POST":

        formset = OrderFormSet(request.POST, instance=customer)

        if formset.is_valid():

            formset.save()

            return redirect("home")

    context = {"formset": formset}

    return render(request, "accounts/order_form.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order)

    if request.method == "POST":

        form = OrderForm(request.POST, instance=order)

        if form.is_valid():

            form.save()

            return redirect("home")

    context = {"form": form}

    return render(request, "accounts/order_form.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def deleteOrder(request, pk):

    order = Order.objects.get(id=pk)

    if request.method == "POST":

        order.delete()

        return redirect("home")

    context = {"item": order}

    return render(request, "accounts/delete.html", context)
