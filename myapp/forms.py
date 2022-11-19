from django import forms
from myapp.models import Order, Client, Product


class OrderForm(forms.ModelForm):
    # order_choices = [(0, 'Order Cancelled'), (1, 'Order Placed'), (2, 'Order Shipped'), (3, 'Order Delivered')]
    # order_status = models.IntegerField(default=1, choices=order_choices)
    client = forms.ModelChoiceField(queryset=Client.objects.all(), label="Client Name", widget=forms.RadioSelect)
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select)
    num_units = forms.IntegerField(label="Quantity")
    # order_status = forms.ChoiceField(widget=forms.RadioSelect, choices=order_choices)
    # status_date = forms.DateField()

    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']


class InterestForm(forms.Form):
    CHOICES = [(1, "Yes"), (0, "No")]
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    quantity = forms.IntegerField(min_value=1, initial=1)
    comments = forms.CharField(widget=forms.Textarea, required=False, label="Additional Comments")

