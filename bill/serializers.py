from rest_framework import serializers

from . models import * 


class CompanySerializer(serializers.ModelSerializer):


    class Meta:

        model = Company

        fields = "__all__"



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
    
        

class CategorySerializer(serializers.ModelSerializer):


 
    class Meta:

        model = Category

        fields = "__all__"


    def get_company_id(self, obj):
        return obj.company.id

    def get_product_name(self, obj):
        return obj.company.name





class CompanyTypeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Company_Types

        fields = "__all__"




class CustomerSerializer(serializers.ModelSerializer):

    
    class Meta:

        model = Customer

        fields = "__all__"



    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('Invoice_No','Customer_id', 'status', 'modes_of_payment', 'total', 'vat', 'subtotal')

    def update(self, instance, validated_data):

        instance.total = validated_data.get('total', instance.total)
        instance.vat = validated_data.get("vat",instance.vat)
        instance.subtotal = instance.total + (instance.total * instance.vat)/ 100
        
        instance.save()  
        return instance
    

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        
        order = instance.Invoice_No
        order_items = OrderItems.objects.filter(Invoice_No=order)

        try:
            subtotal = sum(Decimal(item.product_id.price) * item.quantity for item in order_items)
            print("Subtotal: ", subtotal)
            discount = sum(Decimal(item.discount) for item in order_items)
            print("Discount: ", discount)
            total = subtotal - discount
            print("Total: ", total)
        
            order.subtotal = subtotal
            order.total = total 

            order.save()
        except Decimal.InvalidOperation as e:
            print("Decimal InvalidOperation: ", e)
        return instance
    
