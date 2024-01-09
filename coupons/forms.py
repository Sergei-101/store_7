from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ПРОМОКОД',
                                                         'class': 'form-control',
                                                         'name': 'coupon_code'}))