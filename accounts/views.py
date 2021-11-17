from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .models import *
from django.forms import inlineformset_factory
from .forms import OrderForm, CustomerForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users, admin_Only

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User

from django.contrib import messages
#from django.http import JsonResponce


from django.contrib.auth.decorators import login_required

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user= form.save()
            
            username = form.cleaned_data.get('username')


            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user, name=user.username)


            messages.success(request, f'Account was created for {username}')


            return redirect('login')
    context = {'form':form}
    return render(request, 'templates/accounts/register.html', context)

@unauthenticated_user

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')


    context = {}
    return render(request,'templates/accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')#redirect to login page
@admin_Only
def home(request):

    orders = Order.objects.all().order_by('-id')
    customers = Customer.objects.all()

    totalcustomers = customers.count()
    totalorders = orders.count()
    pending = orders.filter(status='Pending').count()
    delivered = orders.filter(status='Delivered').count()

    context = {'orders': orders, 'customersA': customers, 'totalorders':totalorders, 'pending':pending, 'delivered':delivered}

    return render(request,'templates/accounts/dashboard.html', context)
    '''rendering(returning) data created in form of dictionary list(context) that 
        that can be looped through'''

@login_required(login_url='login')#redirect to login page
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    return render(request, 'templates/accounts/products.html', {'products':products})


@login_required(login_url='login')#redirect to login page
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    totalorders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=(orders))
    orders = myFilter.qs

    context = {'customer':customer, 'orders': orders, 'totalorders': totalorders, 'myFilter': myFilter}
    return render(request, 'templates/accounts/customer.html', context)


@login_required(login_url='login')#redirect to login page
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {'form': form}
    return render(request, 'templates/accounts/create_customer.html', context)


@login_required(login_url='login')#redirect to login page
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {'form': form, 'customer': customer}
    return render(request, 'templates/accounts/update_customer.html', context)

@login_required(login_url='login')#redirect to login page
@allowed_users(allowed_roles=['admin'])
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)

    if request.method == 'POST':
            customer.delete()
            return redirect("/")

    context = {'customer': customer}
    return render(request, 'templates/accounts/delete_customer.html', context)


@login_required(login_url='login')#redirect to login page
@allowed_users(allowed_roles=['admin', 'customer'])
def createOrder(request):
    form = OrderForm()
    #print('Printing POST:', request.POST)
    if request.method == 'POST':
        #if the type of button request is "post"
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {'form':form}
    return render(request, 'templates/accounts/order_form.html', context)


'''
@login_required(login_url='login')#redirect to login page
@allowed_users(allowed_roles=['admin', 'customer'])
def placeNewOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=4)
    customer = Customer.objects.get(id=pk)
    user = request.user.customer.objects.get(id=pk)

    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    formsetss = OrderFormSet(queryset=Order.objects.none(), instance=user)
    #form = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        formsetss = OrderFormSet(request.POST, instance=user)

        if formset.is_valid():
            formset.save()
            return redirect("/")

    context = {'formset':formset, 'customer':customer, 'user':user, 'formsetss':formsetss}
    return render(request, 'templates/accounts/order_form.html', context)
'''

'''
@login_required(login_url='login')#redirect to login page
@allowed_users(allowed_roles=['admin', 'customer'])
def placeNewOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=4)
    
    customer = Customer.objects.get(id=pk)

    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)

        if formset.is_valid():
            formset.save()
            return redirect("/")

    context = {'customer':customer, 'formset':formset}
    return render(request, 'templates/accounts/order_form.html', context)
'''



@login_required(login_url='login')#redirect to login page
@allowed_users(allowed_roles=['admin', 'customer'])
def placeNewOrder(request):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=4)
    
    customer = Customer.objects.get(id=request.user.customer.id)

    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)

        if formset.is_valid():
            formset.save()
            return redirect("/")

    context = {'customer':customer, 'formset':formset}
    return render(request, 'templates/accounts/order_form.html', context)




#pass primary key "pk" when you want to perform action on a specific item
@login_required(login_url='login')#redirect to login page
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    #(instance = order)-> sets the form with the info
    # of the order that you want to update
    #it also updates the current instance (order) instead of
    # creating a new order after submitting

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {'form': form}
    return render(request, 'templates/accounts/order_form.html', context)

@login_required(login_url='login')#redirect to login page
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect("/")

    context = {'item': order}
    return render(request, 'templates/accounts/delete.html', context)


@login_required(login_url='login')#redirect to login page
@allowed_users(allowed_roles=['admin', 'customer'])
def orderSummary(request):
    customer_id = request.user.customer.id

    orders = request.user.customer.order_set.all()
    
    total = 0
    empty = '                                   '
    for i in orders:
        i.product.price
        total = (total+ (i.product.price))
    
    return render(request, 'templates/accounts/order_summary.html', {'orders':orders, 'customer_id':customer_id, 'total':total, 'empty':empty})
    



@login_required(login_url='login')#redirect to login page
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    currentUser = request.user.customer.name

    orders = request.user.customer.order_set.all()

    totalorders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'currentUser':currentUser, 'orders':orders, 'totalorders':totalorders, 'delivered':delivered, 'pending':pending}

    return render(request, 'templates/accounts/user.html', context)



@login_required(login_url='login')#redirect to login page
@allowed_users(allowed_roles=['customer', 'admin'])
def profileSettings(request):
    customer = request.user.customer

    form = CustomerForm(instance=customer)


    context = {'customer': customer, 'forms':form}
    return render(request, 'templates/accounts/profile_settings.html', context)

def updateProfile(request):
    customer = request.user.customer

    form = CustomerForm(instance=customer)


    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'customer': customer, 'forms':form}
    return render(request, 'templates/accounts/profile_settings.html', context)
