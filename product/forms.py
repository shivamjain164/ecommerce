from django import forms
# from .models import Product

class Searchform(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="", widget= forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Search",
    }))
    # This form is used to search for products by name. 
    # It includes a single field 'search' which is a CharField with a maximum length of 100 characters. 
    # The field is not required, meaning the user can submit the form without entering a search term.
    
class Cartform(forms.Form):
    product = forms.CharField(max_length=100, required=False)
    # quantity = forms.IntegerField(min_value=1, required=False, label="Quantity")
    # This form is used to add products to the cart. 
    # It includes two fields: 'product' which is a CharField with a maximum length of 100 characters, 
    # and 'quantity' which is an IntegerField with a minimum value of 1. 
    # Both fields are not required, meaning the user can submit the form without entering any values.
    
class Checkoutform(forms.Form):
    name= forms.CharField(max_length=50, widget = forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Name",
    }))
    email = forms.EmailField(max_length=60, widget=forms.EmailInput(attrs={
        "class":"form-control",
        "placeholder":"Email",
    }))
    address = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Address",
    }))
    city = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"City",
    }))
    state = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"State",
    }))
    zip_code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Zip Code",
    }))
    total = forms.IntegerField(widget=forms.TextInput(attrs={
        "class":"form-control",
        
        }), required=False, label="Total Amount")