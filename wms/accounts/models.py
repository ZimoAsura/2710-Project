from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Region(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Store(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=200, null=True)
	# manager = models.CharField(max_length=200, null=True)
	# sales_number = models.IntegerField()
	region = models.ForeignKey(Region, on_delete=models.PROTECT)
	def __str__(self):
		return self.name

class Sales(models.Model):
	CATEGORY = (
			('Sales', 'Sales'),
			('Store Manager', 'Store Manager'),
			('Region Manager', 'Region Manager'),
			)
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=200, null=True)
	email = models.EmailField(max_length=200, null=True)
	title = models.CharField(max_length=200, choices=CATEGORY)
	store = models.ForeignKey(Store, on_delete=models.PROTECT)
	salary = models.FloatField(default=3000)

	def __str__(self):
		return self.name

class Customer(models.Model):
	CATEGORY = (
			('Home', 'Home'),
			('Business', 'Business'),
			) 
	Gender = (
			('Male', 'Male'),
			('Female', 'Female'),
			) 
	Marriage = (
			('Single', 'Single'),
			('Married', 'Married'),
			) 
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	# required information
	name = models.CharField(max_length=200, null = True)
	email = models.EmailField(max_length=200, null = True)
	phone = models.CharField(max_length=10, null = True)
	address = models.CharField(max_length=200, null = True)
	city = models.CharField(max_length=200, null = True)
	zipcode = models.CharField(max_length=200, null = True)
	kind = models.CharField(max_length=200, choices = CATEGORY, null = True)
	# personal(optional)
	age = models.IntegerField(default=0, null = True)
	income = models.IntegerField(default=0, null = True)
	gender = models.CharField(max_length=200, choices = Gender, null = True)
	marriage = models.CharField(max_length=200, choices = Marriage, null = True)
	# business(optional)
	business =  models.CharField(max_length=200, null = True)
	business_income = models.CharField(max_length=200, null = True)

	def __str__(self):
		return self.name


class Product(models.Model):
	CATEGORY = (
			('Seafood', 'Seafood'),
			('Beauty', 'Beauty'),
			('Wine, Beer & Spirits', 'Wine, Beer & Spirits'),
			('Meat', 'Meat'),
			('Snack', 'Snack'),
			) 

	name = models.CharField(max_length=200)
	price = models.FloatField()
	category = models.CharField(max_length=200, choices=CATEGORY)
	inventory = models.IntegerField(default=100)
	store = models.ForeignKey(Store, on_delete=models.PROTECT, null = True)
	image = models.ImageField(null=True, blank=True)
	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url



class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True, null=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)
	sales = models.ForeignKey(Sales, on_delete=models.PROTECT)

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	product = models.ForeignKey(Product, on_delete= models.PROTECT)
	quantity = models.IntegerField(default=0)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	sales = models.ForeignKey(Sales, on_delete= models.PROTECT)
	
	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total





	
