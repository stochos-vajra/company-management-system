from django.db import models

import random, string


from django.db.models import Sum, F, DecimalField
from decimal import Decimal



def generate_random_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


    

class Company_Types(models.Model):
   

    code = name = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Company(models.Model):
   id = models.CharField(primary_key=True, default=generate_random_id, editable=False, max_length=10)
   name = models.CharField(max_length=100, unique=True)
   email = models.CharField(max_length=50, unique=True)
   phone = models.CharField(max_length=15, unique=True)
   pan_no = models.CharField(max_length=20, unique=True)
   address = models.CharField(max_length=20)
   image = models.ImageField(default="Image Not Found",null=True)
   established = models.DateField()
   company_Type=  models.ForeignKey(Company_Types, on_delete=models.CASCADE,default="Select Company Type")
  

   def __str__(self):
      
      return self.name
   

   
class Category(models.Model):
    id = models.CharField(primary_key=True, default=generate_random_id, editable=False, max_length=10)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,default="")
    image = models.ImageField(null=True)
     
    def __str__(self):
        return self.name

class Product(models.Model):
    Product_id = models.CharField(primary_key=True, default=generate_random_id, editable=False, max_length=10)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=10,default=0)
    image = models.ImageField(null=True)
    created_date = models.DateField(auto_now=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    

class Customer(models.Model):

    Customer_id = models.CharField(primary_key=True, default=generate_random_id, editable=False, max_length=10)

    Customer_Name = models.CharField(max_length=50,default="")

    Customer_phone = models.CharField(max_length=10,unique=True)
    Address = models.CharField(max_length=20, default="")
    Email = models.EmailField(default="example@example.com")
    company = models.ForeignKey(Company, on_delete=models.CASCADE,default="")


    def __str__(self):

        return self.Customer_Name+"--"+self.Customer_phone




class Orders(models.Model):
    
    Invoice_No = models.CharField(primary_key=True, default=generate_random_id, editable=False, max_length=10)
    Customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=10,default="Paid")
    modes_of_payment = models.CharField(max_length=20, default="")
    total = models.IntegerField(default=0)
    vat = models.IntegerField(default=0)
    subtotal = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.Customer_id)
    
    
class OrderItems(models.Model):
    Ordered_Item_Id = models.CharField(primary_key=True, default=generate_random_id, editable=False, max_length=10)
    Invoice_No = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='items')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField()
    discount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Invoice_No)
    

    
