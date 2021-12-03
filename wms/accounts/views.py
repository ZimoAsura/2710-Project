from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, ProductForm, SalesForm, StoreForm
from .filters import OrderFilter, CustomerFilter, SalesFilter, ProductFilter, StoreFilter, RegionFilter

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	# delivered = orders.filter(status='Delivered').count()
	# pending = orders.filter(status='Pending').count()

	products = Product.objects.all()

	context = {'orders':orders, 'products': products, 'customers':customers,
	'total_orders':total_orders}

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def products(request):
	products = Product.objects.all()
	myFilter = ProductFilter(request.GET, queryset=products)
	products = myFilter.qs

	context = {'products':products, 'myFilter':myFilter}
	return render(request, 'accounts/products.html', context)

@login_required(login_url='login')
def store(request):
	stores = Store.objects.all()
	myFilter = StoreFilter(request.GET, queryset=stores)
	stores = myFilter.qs

	context = {'stores':stores, 'myFilter':myFilter}
	return render(request, 'accounts/stores.html', context)

@login_required(login_url='login')
def users_view(request):

	customers = Customer.objects.all()
	myFilter = CustomerFilter(request.GET, queryset=customers)
	customers = myFilter.qs 

	# myFilter = OrderFilter(request.GET, queryset=orders)
	# orders = myFilter.qs 

	context = {'customers':customers, 'myFilter':myFilter}
	return render(request, 'accounts/users.html', context)

@login_required(login_url='login')
def sales_view(request):
	sales = Sales.objects.all()
	myFilter = SalesFilter(request.GET, queryset=sales)
	sales = myFilter.qs

	context = {'sales':sales, 'myFilter':myFilter}
	return render(request, 'accounts/sales.html', context)

@login_required(login_url='login')
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
def region(request):
	regions = Region.objects.all()
	myFilter = RegionFilter(request.GET, queryset=regions)
	regions = myFilter.qs

	context = {'regions':regions, 'myFilter':myFilter}
	return render(request, 'accounts/regions.html', context)

# create/update/delete order
@login_required(login_url='login')
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)

# create/update/delete user
@login_required(login_url='login')
def updateUser(request, pk):

	customer = Customer.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

# create/update/delete product
@login_required(login_url='login')
def createProduct(request):
	context = {}
	if request.method == "GET":
		form = ProductForm()
		context['form'] = form
		return render(request, 'accounts/product_form.html', context)
	
	if request.method == 'POST':
		form = ProductForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/products')

@login_required(login_url='login')
def updateProduct(request, pk):
	product = Product.objects.get(id=pk)
	form = ProductForm(instance=product)

	if request.method == 'POST':
		form = ProductForm(request.POST, instance=product)
		if form.is_valid():
			form.save()
			return redirect('/products')

	context = {'form':form}
	return render(request, 'accounts/product_form.html', context)

@login_required(login_url='login')
def deleteProduct(request, pk):
	product = Product.objects.get(id=pk)
	if request.method == "POST":
		product.delete()
		return redirect('/products')

	context = {'item':product}
	return render(request, 'accounts/delete.html', context)

# create/update/delete sales
@login_required(login_url='login')
def createSales(request):
	context = {}
	if request.method == "GET":
		form = SalesForm()
		context['form'] = form
		return render(request, 'accounts/sales_form.html', context)
	
	if request.method == 'POST':
		form = SalesForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/sales')

@login_required(login_url='login')
def updateSales(request, pk):
	sales = Sales.objects.get(id=pk)
	form = SalesForm(instance=sales)

	if request.method == 'POST':
		form = SalesForm(request.POST, instance=sales)
		if form.is_valid():
			form.save()
			return redirect('/sales')

	context = {'form':form}
	return render(request, 'accounts/sales_form.html', context)

@login_required(login_url='login')
def deleteSale(request, pk):
	sales = Sales.objects.get(id=pk)
	if request.method == "POST":
		sales.delete()
		return redirect('/sales')

	context = {'item':sales}
	return render(request, 'accounts/delete.html', context)

# create/update/delete stores
@login_required(login_url='login')
def createStore(request):
	context = {}
	if request.method == "GET":
		form = StoreForm()
		context['form'] = form
		return render(request, 'accounts/store_form.html', context)
	
	if request.method == 'POST':
		form = StoreForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/stores')

@login_required(login_url='login')
def updateStore(request, pk):
	stores = Store.objects.get(id=pk)
	form = StoreForm(instance=stores)

	if request.method == 'POST':
		form = StoreForm(request.POST, instance=stores)
		if form.is_valid():
			form.save()
			return redirect('/stores')

	context = {'form':form}
	return render(request, 'accounts/store_form.html', context)

@login_required(login_url='login')
def deleteStore(request, pk):
	stores = Store.objects.get(id=pk)
	if request.method == "POST":
		stores.delete()
		return redirect('/stores')

	context = {'item':stores}
	return render(request, 'accounts/delete.html', context)