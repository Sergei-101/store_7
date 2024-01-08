from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity =  quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={
                                                                                    'class': 'qty-control__number text-center',
                                                                                    'type':'number',
                                                                                    'name':'quantity',
                                                                                    'value':'1',
                                                                                    'min':'1'})
    )
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)