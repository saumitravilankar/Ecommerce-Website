from django.urls import path
from . import views


urlpatterns = [
	# path("",views.home,name="home"),
	path("",views.store,name="store"),
	path("cart/",views.cart,name="cart"),
	path("checkout/",views.checkout,name="checkout"),
	path("sign_up/",views.sign_up,name="sign_up"),
	path("add_to_cart/<int:pk>",views.AddToCart.as_view(),name="add_to_cart"),
	path("add_to_inside_cart/<int:pk>",views.AddToInsideCart.as_view(),name="add_to_inside_cart"),
	path("remove_inside_cart/<int:pk>",views.RemoveInsideCart.as_view(),name="remove_inside_cart"),
	path("success/<str:payment_id>",views.payment_success,name="payment_success"),
]