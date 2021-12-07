from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



from .models import *

class OrderForm(ModelForm):
	class Meta:
		model = OrderItem
		fields = '__all__'

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = '__all__'

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

# class CreateCustomerForm(UserCreationForm):
# 	class Meta:
# 		model = Customer
# 		fields = '__all__'

class SalesForm(ModelForm):
	class Meta:
		model = Sales
		fields = '__all__'

class StoreForm(ModelForm):
	class Meta:
		model = Store
		fields = '__all__'

class RegionForm(ModelForm):
	class Meta:
		model = Region
		fields = '__all__'

class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'