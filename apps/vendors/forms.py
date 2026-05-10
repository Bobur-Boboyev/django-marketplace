from django import forms
from .models import Vendor


class VendorAdminForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = "__all__"
\
        widgets = {
            "latitude": forms.TextInput(attrs={"id": "id_latitude"}),
            "longitude": forms.TextInput(attrs={"id": "id_longitude"}),
        }