from django.db import models
from phone_field import PhoneField

# Create your models here.

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
	# required information
	name = models.CharField(max_length=200, null = True)
	email = models.CharField(max_length=200, null = True)
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
	date_created = models.DateTimeField(auto_now_add=True)
	inventory = models.IntegerField(default=100)

	def __str__(self):
		return self.name


class Region(models.Model):
	name = models.CharField(max_length=200)
	# manager = models.ForeignKey(Sales, on_delete=models.PROTECT)

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

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
	product = models.ForeignKey(Product, on_delete= models.PROTECT)
	quantity = models.IntegerField()
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	sales = models.ForeignKey(Sales, on_delete= models.PROTECT)



	
