from django import forms
from .models import Order, OrderItem, PAYMENT_CHOICES
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from django.urls import reverse_lazy
from django.contrib.gis.forms import PointField
from mapwidgets.widgets import GooglePointFieldWidget

User = get_user_model()

class OrderCreateForm(forms.ModelForm):
    location = PointField(widget=GooglePointFieldWidget)
    tel_no = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(
            attrs={'placeholder': 'Your Tel Number:'}),
        label='Country Code',
        initial='+233'
    )
    # preferred_delivery_date = forms.DateField(
    #     widget=forms.DateInput(attrs={'class': 'datepicker'}))
    additional_instructions = forms.CharField(
        widget=forms.TextInput(attrs={'cols': 2, 'rows': 2}), required=False)
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email',
             'tel_no', 'payment_method',
            'additional_instructions', 'location',
        ]
