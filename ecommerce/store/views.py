# for payment integration with razorpay
import razorpay
from django.conf import settings

from django.shortcuts import render,redirect
from .models import Customer,Product,Order,OrderItem,ShippingAddress
from .forms import AddressForm,UserForm
# CVB
from django.views.generic import CreateView,RedirectView

from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# def home(request):

# 	if request.user.is_authenticated:
# 		customer = request.user.customer
# 		order, created = Order.objects.get_or_create(customer=customer,complete=False)

# 	else:
# 		order = {'total_items':0}

# 	return render(request,'store/base.html',{'order':order})

def store(request):

	# item = OrderItem.objects.get(id=15)
	# item.delete()

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)

	products = Product.objects.all()
	return render(request,'store/store.html',{'products':products,
												'order':order})


def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()

	else:
		items=[]
		order = {'orderItems':0,'orderAmount':0}
		cartitems = order['orderItems']

	return render(request,'store/cart.html',{'items': items,
												'order': order})

def checkout(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		# print(order)

	else:
		items=[]
		order = {'orderItems':0,'orderAmount':0}

	# To display saved addresses :
	if request.user.is_authenticated:
		user_with_address = customer.shippingaddress_set.filter(customer=request.user.customer)

	else:
		user_with_address = None

	if request.method == "POST":
		form = AddressForm(request.POST)

		if form.is_valid():
			form = form.save(commit=False)
			form.customer = request.user.customer
			customer = request.user.customer
			form.order = Order.objects.get(customer=customer)
			form.save()
			return redirect('checkout')

		else:
			print(form.errors)
	else:
		form = AddressForm()

	client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))

	try:
		data = { "amount": order.orderAmount * 100, "currency": "INR", "receipt": "order_rcptid_11" ,"payment_capture" : 1}
		payment = client.order.create(data=data)
		order.razor_pay_order_id = payment['id']
		order.save()
		print("*********")
		print(payment)
	except:
		payment = {'amount':100}

	return render(request,'store/checkout.html',{'items': items,
												'order': order,
												'form':form,
												'user_with_address':user_with_address,
												'payment':payment})


def payment_success(request,payment_id):

	if request.user.is_authenticated:
		customer = request.user.customer
		order = Order.objects.get(razor_pay_order_id=payment_id)
		order.complete = True
		order.save()

		order = {'orderItems':0}

	return render(request,'store/payment_success.html',{'order':order})

def sign_up(request):

	if request.method == "POST":
		form =UserForm(request.POST)
		# customer_form = CustomerForm(request.POST)

		if form.is_valid():

			user = form.save()

			Customer.objects.create(customer=user,name=user.username)

			return redirect('login')

		else:
			print(form.errors)
	else:
		form = UserForm()

	return render(request,'store/customer_form.html',{'form':form})

# def add_to_cart(request,pk):

# 	customer = request.user.customer
# 	order, created = Order.objects.get_or_create(customer=customer)
# 	product = Product.objects.get(id=pk)
# 	orderitem = OrderItem.objects.get_or_create(order=order,product=product)
# 	return redirect('store')


class AddToCart(LoginRequiredMixin,RedirectView):

	def get_redirect_url(self,*args,**kwargs):
		customer = self.request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		product = Product.objects.get(id=self.kwargs['pk'])
		orderitem, created = OrderItem.objects.get_or_create(order=order,product=product)
		if orderitem.quantity == 0:
			print("if execute")
			orderitem.quantity = 1
			orderitem.save()
		else:
			print("else execute")
			orderitem.quantity += 1
			orderitem.save()
		return reverse('store')

class AddToInsideCart(RedirectView):

	def get_redirect_url(self,*args,**kwargs):
		customer = self.request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		product = Product.objects.get(id=self.kwargs['pk'])
		orderitem, created = OrderItem.objects.get_or_create(order=order,product=product)
		if orderitem.quantity == 0:
			orderitem.quantity = 1
			orderitem.save()
		else:
			orderitem.quantity += 1
			orderitem.save()
		return reverse('cart')

class RemoveInsideCart(RedirectView):

	def get_redirect_url(self,*args,**kwargs):
		customer = self.request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		product = Product.objects.get(id=self.kwargs['pk'])
		orderitem, created = OrderItem.objects.get_or_create(order=order,product=product)
		if orderitem.quantity < 2:
			orderitem.delete()
		else:
			print("else execute")
			orderitem.quantity -= 1
			orderitem.save()
		return reverse('cart')

