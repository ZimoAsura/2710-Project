import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="date_created", lookup_expr='gte')
	end_date = DateFilter(field_name="date_created", lookup_expr='lte')

	class Meta:
		model = OrderItem
		fields = '__all__'
		exclude = ['customer', 'date_created']

class CustomerFilter(django_filters.FilterSet):
	class Meta:
		model = Customer
		fields = ['name', 'email', 'phone']


class SalesFilter(django_filters.FilterSet):
	class Meta:
		model = Sales
		fields = ['id', 'name', 'email']
		
class ProductFilter(django_filters.FilterSet):
	class Meta:
		model = Product
		fields = ['id', 'name', 'category']

class StoreFilter(django_filters.FilterSet):
	class Meta:
		model = Store
		fields = '__all__'

class RegionFilter(django_filters.FilterSet):
	class Meta:
		model = Region
		fields = '__all__'