from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import datetime

# Create your models here.

class Categories(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name
    

class SubCategory(models.Model):
    Name = models.CharField(max_length=255)
    Category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name
    

class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    


class Product(models.Model):

    Availability = (('In Stock', 'In Stock'),('Out Of Stock', 'Out Of Stock'))

    image = models.ImageField(upload_to='Ecom/Pimg')
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=False, default='')
    subCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=False, default='')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    Availability = models.CharField( choices=Availability , null=True ,max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', error_messages = {'exists':'this email is already exists'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_message['exists'])
        return self.cleaned_data['email']

class contactus(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.name


class order(models.Model):
    image = models.ImageField(upload_to="static/order/image")
    product = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.CharField(max_length=5)
    total = models.CharField(max_length=255, default='')
    address = models.TextField()
    phone = models.CharField(max_length=12)
    pincode = models.CharField(max_length=30)
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return self.product
    
    