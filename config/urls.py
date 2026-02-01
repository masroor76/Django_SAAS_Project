from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/subscriptions/', include('subscriptions.subscriptions_url')),
    path('api/v1/organizations/', include('organizations.organizations_url')),
    path('api/v1/orders/', include('orders.orders_url')),
    path('api/v1/customers/', include('customers.customers_urls')),
    path('api/v1/analytics/', include('analytics.analytics_urls')),
    path('api/v1/auth/', include('accounts.auth_urls')),
    path('api/v1/verify/', include('verifications.verifications_urls')),
]
