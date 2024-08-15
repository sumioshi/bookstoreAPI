import debug_toolbar
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
    path("admin/", admin.site.urls),
    re_path(r"bookstore/(?P<version>(v1|v2))/", include("order.urls")),
    re_path(r"bookstore/(?P<version>(v1|v2))/", include("product.urls")),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
