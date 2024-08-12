import debug_toolbar
from django.urls import path, re_path, include
from django.contrib import admin

urlpatterns = [
    path('__dbug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    re_path(r'bookstore/(?P<version>(v1|v2))/', include('order.urls')),
    re_path(r'bookstore/(?P<version>(v1|v2))/', include('product.urls')),
]
