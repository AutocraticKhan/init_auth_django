from django import forms
from .models import Business, Location, Category, Tag, Amenity, PaymentMethod, AccessibilityFeature

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        exclude = ('created_at', 'updated_at',)

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = '__all__'
        exclude = ('slug', 'claimed_by_user', 'average_rating', 'review_count', 'is_claimed', 'is_verified', 'verification_details', 'status', 'created_at', 'updated_at', 'location', 'secondary_categories', 'tags', 'amenities', 'payment_methods', 'accessibility_features')

    # Add fields for ManyToMany relationships if needed in Phase 1, but for now, exclude them.
    # primary_category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    # tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    # amenities = forms.ModelMultipleChoiceField(queryset=Amenity.objects.all(), required=False)
    # payment_methods = forms.ModelMultipleChoiceField(queryset=PaymentMethod.objects.all(), required=False)
    # accessibility_features = forms.ModelMultipleChoiceField(queryset=AccessibilityFeature.objects.all(), required=False)
