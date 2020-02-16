from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('home', views.product_list, name='home'),
    path('cart/<slug>', views.add_to_cart, name='cart'),
    # path('remove/<slug>', views.remove_from_cart, name='remove-cart'),
    path('cart_items', views.cartview, name='cart_items'),
    path('decrease-cart/<slug>', views.decreasecart, name='decrease-cart'),
    path('increase-cart/<slug>', views.increasecart, name='increase-cart'),
    # path('save-address/', views.checkoutview, name="save-address"),
    path('signup', views.signup, name='signup'),
    path('login', views.user_login, name='login'),
    path('logout', views.logout_request, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
