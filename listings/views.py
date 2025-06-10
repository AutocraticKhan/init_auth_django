from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BusinessForm, LocationForm
from .models import Business, Location, Category # Import Category for primary_category field

class AddBusinessListingView(LoginRequiredMixin, View):
    template_name = 'listings/add_business.html'

    def get(self, request, *args, **kwargs):
        business_form = BusinessForm()
        location_form = LocationForm()
        return render(request, self.template_name, {
            'business_form': business_form,
            'location_form': location_form
        })

    def post(self, request, *args, **kwargs):
        business_form = BusinessForm(request.POST)
        location_form = LocationForm(request.POST)

        if business_form.is_valid() and location_form.is_valid():
            location_instance = location_form.save()
            business_instance = business_form.save(commit=False)
            business_instance.location = location_instance
            business_instance.claimed_by_user = request.user # Assign the current logged-in user
            business_instance.save()
            # Handle ManyToMany fields after saving the business instance
            # For now, these are excluded in the form, but if they were included:
            # business_form.save_m2m()

            return redirect('add_business_success') # Redirect to a success page or the business detail page
        else:
            return render(request, self.template_name, {
                'business_form': business_form,
                'location_form': location_form
            })

class AddBusinessSuccessView(View):
    template_name = 'listings/add_business_success.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
