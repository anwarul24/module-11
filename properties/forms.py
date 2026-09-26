from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            "title",
            "description",
            "property_type",
            "location",
            "monthly_rent",
            "bedrooms",
            "bathrooms",
            "image",
            "is_available",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "property_type": forms.Select(attrs={"class": "form-select"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "monthly_rent": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "bedrooms": forms.NumberInput(attrs={"class": "form-control"}),
            "bathrooms": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class PropertySearchForm(forms.Form):
    location = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "Location"})
    )
    property_type = forms.ChoiceField(
        required=False,
        choices=[("", "Any type")] + list(Property.PropertyType.choices),
    )
    min_rent = forms.DecimalField(
        required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder": "Min rent"})
    )
    max_rent = forms.DecimalField(
        required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder": "Max rent"})
    )

    def clean(self):
        cleaned_data = super().clean()
        min_rent = cleaned_data.get("min_rent")
        max_rent = cleaned_data.get("max_rent")
        if min_rent is not None and max_rent is not None and min_rent > max_rent:
            raise forms.ValidationError("Minimum rent cannot be greater than maximum rent.")
        return cleaned_data
