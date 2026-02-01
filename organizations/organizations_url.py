from django.urls import path
from .views import CreateOrganization_View , ChangeOwnerOrganizationView

urlpatterns=[
    path('create-organization/', CreateOrganization_View.as_view(), name='create-organization'),
    path('<int:org_id>/change-owner-organization/', ChangeOwnerOrganizationView.as_view(), name='change-owner-organization'),
]