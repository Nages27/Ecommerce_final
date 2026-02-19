from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('electronics/', views.electronics, name='electronics'),
    path('view/<int:id>/', views.view, name='view'),
    path('add/<int:id>/', views.add_to_cart, name='add'),
    path('cart/', views.view_cart, name='view_cart'),
   path('place_order/', views.place_order, name='place_order'),
    path('place_order/<int:item_id>/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:id>/',views.order,name='order'),
    path('cart/increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('pl_order',views.pl_order,name='pl_order'),
    #path('update/<int:id>/<str:action>/', views.update_cart, name='update_cart'),

]
    


