from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	customer = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True,default='AnonymousUser')
	name = models.CharField(max_length=200,null=True,blank=True,default='anonymous')

	def __str__(self):
		return self.customer.username

class Product(models.Model):
	name = models.CharField(max_length=2000,null=True)
	price = models.IntegerField()
	image = models.ImageField(upload_to='products',blank=True,null=True)

	def __str__(self):
		return self.name

	@property
	def productImage(self):
		try:
			url = self.image.url
		except:
			url = 'static/images/default_product.png'
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True,null=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False,null=True,blank=True)
	transaction_id = models.CharField(max_length=200,null=True,blank=True)
	razor_pay_payment_id = models.CharField(max_length=100,null=True,blank=True)
	razor_pay_order_id = models.CharField(max_length=100,null=True,blank=True)
	razor_pay_payment_signature = models.CharField(max_length=100,null=True,blank=True)

	@property
	def orderItems(self):
		total_items = self.orderitem_set.all()
		total_quantity = sum([item.quantity for item in total_items])
		return total_quantity

	@property
	def orderAmount(self):
		total_items = self.orderitem_set.all()
		total_amount = sum([item.itemTotal for item in total_items])
		return total_amount

	def __str__(self):
		return self.customer.name + ' ' + str(self.id)

class OrderItem(models.Model):
	order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
	product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
	quantity = models.IntegerField(default=0,blank=True,null=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def itemTotal(self):
		total = self.product.price * self.quantity
		return total

	@property
	def add_quantity(self):
		return self.quantity + 1

	def __str__(self):
		return self.product.name + " " + self.order.customer.name + str(self.id)

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
	order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
	name = models.CharField(max_length=200,null=True)
	address = models.TextField(max_length=2000,null=True)
	city = models.CharField(max_length=25, null=True)
	state = models.CharField(max_length=25, null=True)
	zipcode = models.CharField(max_length=10, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name
