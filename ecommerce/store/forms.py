from django import forms
from .models import ShippingAddress, Customer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):

	class Meta:
		model = User
		fields = ['username','email','password1','password2']

# class CustomerForm(forms.ModelForm):

# 	class Meta:
# 		model = Customer
# 		fields = ("name",)

class AddressForm(forms.ModelForm):

	class Meta:

		model = ShippingAddress
		fields = ["name","address","city","state","zipcode"]
