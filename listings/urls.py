from django.urls import path
from .views import AddBusinessListingView, AddBusinessSuccessView

urlpatterns = [
    path('add/', AddBusinessListingView.as_view(), name='add_business_listing'),
    path('add/success/', AddBusinessSuccessView.as_view(), name='add_business_success'),
]
