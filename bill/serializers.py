from rest_framework import serializers

from . models import * 


class CompanySerializer(serializers.ModelSerializer):

    # company_type = serializers.CharField(source="company_Type.name", read_only=True)

    class Meta:

        model = Company

        fields = "__all__"



class ProductSerializer(serializers.ModelSerializer):
    # company_id = serializers.SerializerMethodField()
    # company_name = serializers.SerializerMethodField()
    # category_id = serializers.SerializerMethodField()
    # category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        # fields = ["Product_id", "name", "price", "image", "created_date", "updated_date", "active", "company_id", "company_name", "category_id", "category_name"]
        fields = "__all__"
    
        

class CategorySerializer(serializers.ModelSerializer):

    # company = serializers.CharField(source="company.name",read_only=True)
    # company_id = serializers.SerializerMethodField()
 
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


# class OrderSerializer(serializers.ModelSerializer):


#     class Meta:
#         model = Orders
#         fields = '__all__'

# class OrderSerializer(serializers.ModelSerializer):
#     vat_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, write_only=True)
#     final_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

#     class Meta:
#         model = Orders  # Assuming your model is named Order
#         fields = "__all__"

    
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
    
