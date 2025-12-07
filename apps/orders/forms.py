from django import forms

from apps.curbside.models import PickupSlot


class CheckoutForm(forms.Form):
    pickup_slot = forms.ModelChoiceField(
        queryset=PickupSlot.objects.none(),
        empty_label="Select a pickup window",
    )
    notes = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pickup_slot"].queryset = PickupSlot.objects.upcoming()
