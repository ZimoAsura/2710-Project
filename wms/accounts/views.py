from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponse
from django.contrib import messages


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
import random

from django.contrib import messages
from django.db.models import Sum,F,Count

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, ProductForm, SalesForm, StoreForm, RegionForm, CustomerForm
from .filters import OrderFilter, CustomerFilter, SalesFilter, ProductFilter, StoreFilter, RegionFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
from .utils import *
import datetime


def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
	
	context = {'form':form}
	return render(request, 'accounts/register.html', context)

def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user:
			login(request, user)
			group = user.groups.all()[0].name
			print(group)
			if group == 'customer':
				return redirect('store_list')
			if group == 'admin':
				return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
	orders = OrderItem.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	total_quantity = orders.aggregate(sum=Sum('quantity'))
	total_sales = orders.aggregate(sum=Sum(F('quantity') * F('product__price')))
	# delivered = orders.filter(status='Delivered').count()
	# pending = orders.filter(status='Pending').count()

	products = Product.objects.all()

	category_agg = (Product.objects.values('category')) \
		.annotate(sum_quantity=Sum('orderitem__quantity')).order_by('-sum_quantity')

	for obj in category_agg:
		if not obj['sum_quantity']:
			obj['sum_quantity'] = 0
	
	product_agg = (Product.objects.values('name')) \
		.annotate(sum_quantity=Sum('orderitem__quantity'), sum=Sum(F('orderitem__quantity') * F('price'))).order_by('-sum_quantity')
	
	for obj in product_agg:
		if not obj['sum_quantity']:
			obj['sum_quantity'] = 0
		if not obj['sum']:
			obj['sum'] = 0
		obj['sum'] = round(obj['sum'],2)
	
	customer_agg = (Customer.objects.values('name')) \
		.annotate(sum_quantity=Sum('orderitem__quantity')).order_by('-sum_quantity')
	
	region_agg = Region.objects\
		.annotate(sum_quantity=Sum('store__sales__orderitem__quantity')).order_by('-sum_quantity')
	
	for obj in region_agg:
		if not obj.sum_quantity:
			obj.sum_quantity = 0
			
	context = {'orders': orders, 'products': products, 'customers': customers,
			   'total_orders': total_orders, 'total_quantity': total_quantity, 'total_sales':round(total_sales['sum'],2),
			   'category_result': category_agg, 'product_result':product_agg,'customer_result':customer_agg, 'region_result': region_agg}

	return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def products(request):
	products = Product.objects.all()
	myFilter = ProductFilter(request.GET, queryset=products)
	products = myFilter.qs

	context = {'products': products, 'myFilter': myFilter}
	return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def store(request):
	stores = Store.objects.all()
	myFilter = StoreFilter(request.GET, queryset=stores)
	stores = myFilter.qs

	context = {'stores': stores, 'myFilter': myFilter}
	return render(request, 'accounts/stores.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def users_view(request):
	customers = Customer.objects.all()
	myFilter = CustomerFilter(request.GET, queryset=customers)
	customers = myFilter.qs

	# myFilter = OrderFilter(request.GET, queryset=orders)
	# orders = myFilter.qs

	context = {'customers': customers, 'myFilter': myFilter}
	return render(request, 'accounts/users.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def sales_view(request):
	sales = Sales.objects.all()
	myFilter = SalesFilter(request.GET, queryset=sales)
	sales = myFilter.qs

	context = {'sales': sales, 'myFilter': myFilter}
	return render(request, 'accounts/sales.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.orderitem_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs

	context = {'customer': customer, 'orders': orders, 'order_count': order_count,
			   'myFilter': myFilter}
	return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def region(request):
	regions = Region.objects.all()
	myFilter = RegionFilter(request.GET, queryset=regions)
	regions = myFilter.qs

	context = {'regions': regions, 'myFilter': myFilter}
	return render(request, 'accounts/regions.html', context)


# create/update/delete product
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def createRegion(request):
	context = {}
	if request.method == "GET":
		form = RegionForm()
		context['form'] = form
		return render(request, 'accounts/region_form.html', context)

	if request.method == 'POST':
		form = RegionForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/regions')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def deleteRegion(request, pk):
	regions = Region.objects.get(id=pk)
	if request.method == "POST":
		try:
			regions.delete()
			return redirect('/regions')
		except:
			messages.info(request, f'Failed to delete. {regions.name} is a foreign key in other tables')
			return redirect('/regions')

	context = {'item': regions}
	return render(request, 'accounts/delete_region.html', context)


# create/update/delete order
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, OrderItem, 
										 fields=('product', 'quantity', 'sales'), extra=10)
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=OrderItem.objects.none(), instance=customer)
	# form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		# print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/users')

	context = {'form': formset}
	return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def updateOrder(request, pk):
	order = OrderItem.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form': form}
	return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def deleteOrder(request, pk):
	order = OrderItem.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item': order}
	return render(request, 'accounts/delete.html', context)


# create/update/delete user
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def createUser(request):
	context = {}
	if request.method == "GET":
		form = CustomerForm()
		context['form'] = form
		return render(request, 'accounts/customer_form.html', context)

	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/users')
		
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def updateUser(request, pk):
	customers = Customer.objects.get(id=pk)
	form = CustomerForm(instance=customers)

	if request.method == 'POST':
		form = CustomerForm(request.POST, instance=customers)
		if form.is_valid():
			form.save()
			return redirect(f'/customer/{pk}')

	context = {'form': form}
	return render(request, 'accounts/customer_form.html', context)


# create/update/delete product
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
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
@allowed_users(allowed_roles=['admin'])
@admin_only
def updateProduct(request, pk):
	product = Product.objects.get(id=pk)
	form = ProductForm(instance=product)

	if request.method == 'POST':
		form = ProductForm(request.POST, instance=product)
		if form.is_valid():
			form.save()
			return redirect('/products')

	context = {'form': form}
	return render(request, 'accounts/product_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def deleteProduct(request, pk):
	product = Product.objects.get(id=pk)
	if request.method == "POST":
		try:
			product.delete()
		except:
			messages.info(request, f'Failed to delete. {product.name} is a foreign key in other tables')

		return redirect('/products')

	context = {'item': product}
	return render(request, 'accounts/delete_product.html', context)


# create/update/delete sales
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
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
@allowed_users(allowed_roles=['admin'])
@admin_only
def updateSales(request, pk):
	sales = Sales.objects.get(id=pk)
	form = SalesForm(instance=sales)

	if request.method == 'POST':
		form = SalesForm(request.POST, instance=sales)
		if form.is_valid():
			form.save()
			return redirect('/sales')

	context = {'form': form}
	return render(request, 'accounts/sales_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def deleteSale(request, pk):
	sales = Sales.objects.get(id=pk)
	if request.method == "POST":
		try:
			sales.delete()
		except:
			messages.info(request, f'Failed to delete. {sales.name} is a foreign key in other tables')


		return redirect('/sales')

	context = {'item': sales}
	return render(request, 'accounts/delete_sale.html', context)


# create/update/delete stores
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
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
@allowed_users(allowed_roles=['admin'])
@admin_only
def updateStore(request, pk):
	stores = Store.objects.get(id=pk)
	form = StoreForm(instance=stores)

	if request.method == 'POST':
		form = StoreForm(request.POST, instance=stores)
		if form.is_valid():
			form.save()
			return redirect('/stores')

	context = {'form': form}
	return render(request, 'accounts/store_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def deleteStore(request, pk):
	stores = Store.objects.get(id=pk)
	if request.method == "POST":
		stores.delete()
		return redirect('/stores')

	context = {'item': stores}
	return render(request, 'accounts/delete_store.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def user_store(request, pk=None): # pk is sales id
	data = cartData(request, pk)
	if not data:
		return HttpResponse("Not allowed")
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	sale_store = Sales.objects.values_list('store', flat=True).get(id=pk)
	print(sale_store)
	products = Product.objects.filter(store = sale_store).all()
	context = {'products':products, 'cartItems':cartItems, 'sales':data['sales']}
	return render(request, 'store/storeProducts.html', context)

@login_required(login_url='login')
def cart(request, pk=None):
	data = cartData(request, pk)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems, 'sales':data['sales']}
	return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, pk=None):
	data = cartData(request, pk)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems, 'sales':data['sales']}
	return render(request, 'store/checkout.html', context)


@login_required(login_url='login')
def store_list(request):
	sales = Sales.objects.all()
	context = {'sales': sales}
	return render(request, 'store/salesList.html', context)


@login_required(login_url='login')
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	salesId = data['salesId']
 
	customer = request.user.customer

	product = Product.objects.get(id=productId)
	sales = Sales.objects.get(id=salesId)

	order, created = Order.objects.get_or_create(customer=customer, sales = sales, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, customer=customer, sales=sales)
	 
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


@login_required(login_url='login')
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	salesId = data['form']['salesId']
	sales = Sales.objects.get(id=salesId)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, sales = sales,complete=False)


	total = float(data['form']['total'])
	order.transaction_id = transaction_id
	# update item
	order.date_ordered = datetime.datetime.now()

	if total == order.get_cart_total:
		order.complete = True
  
	# modify inventory
	for item in order.orderitem_set.all():
		
		if (item.product.inventory < item.quantity):
			return JsonResponse(f"{item.product.name} inventory is not enough, \n only {item.product.inventory} left", safe=False)
		item.product.inventory -= item.quantity
		item.date_created = order.date_ordered
		item.product.save()	
	
	order.save()

	return JsonResponse('Successful', safe=False)

@login_required(login_url='login')
def order_history(request, pk):
	customer = Customer.objects.get(id=pk)

	orders = customer.orderitem_set.all()
	orders = orders.filter(order__complete=True).order_by('-date_created')
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs
 
	transactions = customer.order_set.all()
	

	context = {'customer': customer, 'orders': orders, 'order_count': order_count,
			   'myFilter': myFilter, 'transactions': transactions}
	return render(request, 'store/order_history.html', context)

@login_required(login_url='login')
def user_updateUser(request, pk):
	customers = Customer.objects.get(id=pk)
	form = CustomerForm(instance=customers)

	if request.method == 'POST':
		form = CustomerForm(request.POST, instance=customers)
		if form.is_valid():
			form.save()
			return redirect(f'/order_history/{pk}')

	context = {'form': form}
	return render(request, 'store/user_customer_form.html', context)