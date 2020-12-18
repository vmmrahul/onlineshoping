"""onlineShoping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from view import *
urlpatterns = [
    path('myadmin/', admin.site.urls),
    path('addCateogryPage', addCateogryPage),
    path('addCategoryAction', addCategoryAction),
    path('viewCateogrypage', viewCateogrypage),
    path('deleteCategory', deleteCategory),
    path('editCateogry', editCateogry),
    path('editCategoryAction', editCategoryAction),
    path('addproduct', addproduct),
    path('view_product', view_product),

    # client side url
    path('', index),
    path('viewCateogry', viewCateogry),
    path('viewProduct', viewProduct),
    path('cartCheckout', cartCheckout, name='cartcheckout'),
    path('add_to_cart', add_to_cart),
    path('cart_inc_dec', cart_inc_dec),
    path('process_to_pay', process_to_pay),
    path('payment_action', payment_action),
    path('thankspage', thankspage),
    path('contactUs', contactUs, name='mailUs'),

]
