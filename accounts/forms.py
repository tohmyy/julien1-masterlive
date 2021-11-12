from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm

from .models import Order
from .models import Customer
from django.contrib.auth.models import User



class OrderForm(ModelForm):
    class Meta:
         model = Order
         fields = '__all__'#allows me to import all fields(models)
         # (customer field, product field, status field (model))

class CustomerForm(ModelForm):
    class Meta:
        model = Customer

        fields = "__all__"
        exclude =['user'] #disable customers from editing user/customer relationship

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']



