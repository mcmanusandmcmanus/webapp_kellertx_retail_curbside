from django import forms

from .models import ArrivalAlert


class ArrivalAlertForm(forms.ModelForm):
    class Meta:
        model = ArrivalAlert
        fields = ("vehicle_desc", "parking_spot")
        widgets = {
            "vehicle_desc": forms.TextInput(attrs={"placeholder": "Vehicle description"}),
            "parking_spot": forms.TextInput(attrs={"placeholder": "Parking spot (optional)"}),
        }
