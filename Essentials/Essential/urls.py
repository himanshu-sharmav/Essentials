from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


# from .middlewares.auth import auth_middleware 
# from .views.register import register

urlpatterns =[
    path('register/', views.register, name='register'),
    path('custom_login/',views.custom_login,name='custom_login'),
    path('add_section/', views.add_section, name='add_section'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/',views.edit_product,name ='edit_product'),
    path('edit_section/<int:section_id>/', views.edit_section, name='edit_section'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('buy_products/',views.buy_products,name='buy_products'),
    path('search_sections/',views.search_sections,name='search_sections'),
    path('search_products/',views.search_products,name='search_products')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)