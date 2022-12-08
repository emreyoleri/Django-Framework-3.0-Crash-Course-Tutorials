from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from .models import *
from .forms import OrderForm
from .filters import OrderFilter


def login(request):

    context = {}

    return render(request, "accounts/login.html", context)


def register(request):

    form = UserCreationForm()

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

    context = {"form": form}

    return render(request, "accounts/register.html", context)


def home(request):

    orders = Order.objects.all()

    customers = Customer.objects.all()

    total_orders = orders.count()

    total_customers = customers.count()

    delivered = orders.filter(status="Delivered").count()

    pending = orders.filter(status="Pending").count()

    context = {"orders": orders, "customers": customers,
               "total_orders": total_orders, "total_customers": total_customers, "delivered": delivered, "pending": pending}

    return render(request, "accounts/dashboard.html", context)


def products(request):

    products = Product.objects.all()

    context = {"products": products}

    return render(request, "accounts/products.html", context)


def customer(request, pk):

    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()

    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)

    orders = myFilter.qs

    context = {"customer": customer, "orders": orders,
               "total_orders": total_orders, "myFilter": myFilter}

    return render(request, "accounts/customer.html", context)


def createOrder(request, pk):

    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=("product", "status"), extra=3)

    customer = Customer.objects.get(id=pk)

    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    # form = OrderForm(initial={"customer": customer})

    if request.method == "POST":

        # form = OrderForm(request.POST)

        formset = OrderFormSet(request.POST, instance=customer)

        if formset.is_valid():

            formset.save()

            return redirect("home")

    # context = {"form": form}

    context = {"formset": formset}

    return render(request, "accounts/order_form.html", context)


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


def deleteOrder(request, pk):

    order = Order.objects.get(id=pk)

    if request.method == "POST":

        order.delete()

        return redirect("home")

    context = {"item": order}

    return render(request, "accounts/delete.html", context)
