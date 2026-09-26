from django import forms
from .models import RentalRequest


class RentalRequestForm(forms.ModelForm):
    class Meta:
        model = RentalRequest
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Introduce yourself to the owner..."}
            ),
        }
