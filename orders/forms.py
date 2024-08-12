from django import forms
from orders.models import Order



# class OrderCreateForm(forms.ModelForm):
#     first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов'}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}))
#     phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+375(29)1112233'}))
#     address = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'form-control', 'placeholder': 'РБ, Минск, ул. Мира, дом 6',
#     }))
#     description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Примечание к заказу'}))
#
#
#     class Meta:
#         model = Order
#         fields = ('first_name', 'last_name', 'email', 'address')

class PersonalOrderForm(forms.ModelForm):
    contact_person = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ФИО'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес доставки'}), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+375(29)1112233'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Примечание к заказу'}), required=False)



    class Meta:
        model = Order
        fields = ['contact_person', 'address', 'email', 'phone_number', 'description']
        labels = None

class BusinessOrderForm(forms.ModelForm):
    company_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название компании'}))
    unp = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'УНП'}))
    checking_account = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Расчетный счет'}))
    bic = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Бик банка'}))
    bank_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наименование банка'}))
    legal_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Юридический адрес'}))
    contact_person = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Контактное лицо'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес доставки'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+375(29)1112233'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Примечание к заказу'}))


    class Meta:
        model = Order
        fields = ['company_name', 'unp', 'checking_account', 'bic', 'bank_name', 'legal_address', 'contact_person', 'address', 'email', 'phone_number', 'description']
        labels = None

