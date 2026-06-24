from django.shortcuts import render

from . models import *
from django.http import Http404

from .serializers import *

from rest_framework  import viewsets, status

from rest_framework.decorators import api_view

from rest_framework.response import Response

from django.db.models import Q

from rest_framework.views import APIView

class CompanyViewset(viewsets.ModelViewSet):

    queryset=Company.objects.all()

    serializer_class = CompanySerializer


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        org_name = request.query_params.get('org_name')
        if not org_name:
            return Response({"error": "org_name query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(name=org_name)
        except Company.DoesNotExist:
            raise Http404("Company does not exist")

        categories = Category.objects.filter(company=company.id)
        if not categories.exists():
            return Response({"message": "No categories found for the given company"}, status=status.HTTP_200_OK)

        category_serializer = CategorySerializer(categories, many=True)

        return Response(category_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        org_name = request.query_params.get('org_name')
        if not org_name:
            return Response({"error": "org_name query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(name=org_name)
        except Company.DoesNotExist:
            raise Http404("Company does not exist")

        categories = Category.objects.filter(company=company.id)
        if not categories.exists():
            return Response({"message": "No categories found for the given company"}, status=status.HTTP_200_OK)

        category_serializer = CategorySerializer(categories, many=True)
        products = Product.objects.filter(company=company.id)
        product_serializer = ProductSerializer(products, many=True)

        response_data = {
            "categories": category_serializer.data,
            "products": product_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    


class CompanyTypeListCreate(APIView):
    def get(self, request, format=None):
        company_types = Company_Types.objects.all()
        serializer = CompanyTypeSerializer(company_types, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CompanyTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    







class CompanyListCreate(APIView):
    def get(self, request, org_name=None, format=None):
        if org_name:
            companies = Company.objects.filter(name=org_name)
        else:
            companies = Company.objects.all()

        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





class ProductDataListCreate(APIView):
    def get(self, request, org_name, format=None):
        try:
            company = Company.objects.get(name=org_name)
        except Company.DoesNotExist:
            raise Http404("Company does not exist")

        categories = Category.objects.filter(company=company.id)
        items = Product.objects.filter(company=company.id, category__in=categories)
        serializer = ProductSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, org_name, format=None):
        try:
            company = Company.objects.get(name=org_name)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        categories = Category.objects.filter(company=company)

        if not categories.exists():
            return Response({"message": "No categories found for the given company"}, status=status.HTTP_404_NOT_FOUND)

        category_ids = [category.id for category in categories]
        request_category_id = request.data.get('category', None)

        if request_category_id not in category_ids:
            return Response({"error": "Category does not belong to the company"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        





class CategoryDataListCreate(APIView):
    def get(self, request, org_name, format=None):
        try:
            company = Company.objects.get(name=org_name)
        except Company.DoesNotExist:
            raise Http404("Company does not exist")

        categories = Category.objects.filter(company=company.id)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, org_name, format=None):
        try:
            company = Company.objects.get(name=org_name)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['company'] = company.id

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomerDataListCreate(APIView):
    def get(self, request, org_name, format=None):
        try:
            company = Company.objects.get(name=org_name)
        except Company.DoesNotExist:
            raise Http404("Company does not exist")

        customers = Customer.objects.filter(company=company.id)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request, org_name, format=None):
        try:
            company = Company.objects.get(name=org_name)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['company'] = company.id

        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class CustomerOrderDetail(APIView):
    def post(self, request, cid, format=None):
        try:
            customer = Customer.objects.get(Customer_id=cid)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        request.data['Customer_id'] = cid


        serializer = OrderSerializer(data=request.data)


        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, cid, format=None):
        try:
            customer = Customer.objects.get(Customer_id=cid)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        orders = Orders.objects.filter(Customer_id=cid)  

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


    def put(self, request, cid, format=None):
        try:
            order = Orders.objects.get(Customer_id=cid)
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Orders.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)



class OrderItemDetail(APIView):
    def post(self, request, invoice_no, format=None):
        try:
            order = Orders.objects.get(Invoice_No=invoice_no)
        except Orders.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderItemsSerializer(data=request.data)

        if serializer.is_valid():

            customer = order.Customer_id


            company = customer.company


            company_products = Product.objects.filter(company=company)


            product_id = request.data.get('product_id')
            if not company_products.filter(Product_id=product_id).exists():
                return Response({'error': 'Product does not belong to your company'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(Invoice_No=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, invoice_no, format=None):
        try:
            order = Orders.objects.get(Invoice_No=invoice_no)
            order_items = OrderItems.objects.filter(Invoice_No=order)
            serializer = OrderItemsSerializer(order_items, many=True)
            return Response(serializer.data)
        except Orders.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class OrdersDataListCreate(APIView):

    def get(self, request, org_name, format=None):
        try:
            company = Company.objects.get(name=org_name)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        customers = Customer.objects.filter(company=company)
        orders = Orders.objects.filter(Customer_id__in=customers)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    # def post(self, request, org_name, format=None):
    #     try:
    #         company = Company.objects.get(name=org_name)
    #     except Company.DoesNotExist:
    #         return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    #     categories = Category.objects.filter(company=company)

    #     if not categories.exists():
    #         return Response({"message": "No categories found for the given company"}, status=status.HTTP_404_NOT_FOUND)

    #     category_ids = [category.id for category in categories]
    #     request_category_id = request.data.get('category', None)

    #     if request_category_id not in category_ids:
    #         return Response({"error": "Category does not belong to the company"}, status=status.HTTP_400_BAD_REQUEST)

    #     serializer = ProductSerializer(data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def show(request):

    return render(request,"company_list.html")

def home(request):

    return render(request,"prep.html")



""" 

@api_view(['POST'])
def addCompany_Type(request):
    serializer = CompanyTypeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201) 
    else:
        return Response(serializer.errors, status=400)

@api_view(['GET'])
def getCompany_Type(request):

    company = Company_Types.objects.all()


    serializer = CompanyTypeSerializer(company, many=True)
    return Response(serializer.data)


"""




    
""

""" 
@api_view(['POST'])
def addCompany(request):
    serializer = CompanySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201) 
    else:
        return Response(serializer.errors, status=400)

@api_view(['GET'])
def getCompanyData(request, org_name):

    company = Company.objects.filter(name=org_name)


    serializer = CompanySerializer(company, many=True)
    return Response(serializer.data)
"""

""" 
@api_view(['POST'])
def addProductData(request, org_name):
    try:
        # Get the company object based on the org_name
        company = Company.objects.get(name=org_name)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get categories associated with the company
    categories = Category.objects.filter(company=company)

    if not categories.exists():
        return Response({"message": "No categories found for the given company"}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the list of categories
    category_serializer = CategorySerializer(categories, many=True)

    # Check if the category provided in request data belongs to the company
    category_ids = [category.id for category in categories]
    request_category_id = request.data.get('category', None)

    if request_category_id not in category_ids:
        return Response({"error": "Category does not belong to the company"}, status=status.HTTP_400_BAD_REQUEST)

    # Proceed with product data addition
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
def getProductData(request, org_name):
    try:
        company = Company.objects.get(name=org_name)
    except Company.DoesNotExist:
        raise Http404("Company does not exist")

    categories = Category.objects.filter(company=company.id)

    # Now fetch products based on company and categories
    items = Product.objects.filter(company=company.id, category__in=categories)
    serializer = ProductSerializer(items, many=True)
    return Response(serializer.data)

"""

# @api_view(['POST'])
# def addCategoryData(request):
#     serializer = CategorySerializer(data=request.data)

#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201) 
#     else:
#         return Response(serializer.errors, status=400)
    
# @api_view(['GET'])
# def getCategoryData(request, org_name):
#     try:
#         companies = Company.objects.get(name=org_name)
#         category = Category.objects.filter(company=companies.id)
#         serializer = CategorySerializer(category, many=True)
#         return Response(serializer.data)
#     except Company.DoesNotExist:
#         raise Http404("Company does not exist")




# class CustomerOrderDetail(APIView):
#     def post(self, request, invoice_no, format=None):
#         try:
#             order = Orders.objects.get(Invoice_No=invoice_no)
#             serializer = OrderSerializer(order, data=request.data)
#         except Orders.DoesNotExist:
#             # If order does not exist, create a new one
#             request.data['Invoice_No'] = invoice_no
#             serializer = OrderSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED if not order else status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, invoice_no, format=None):
#         try:
#             order = Orders.objects.get(Invoice_No=invoice_no)
#         except Orders.DoesNotExist:
#             return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = OrderSerializer(order)
#         return Response(serializer.data)

#     def put(self, request, invoice_no, format=None):
#         try:
#             order = Orders.objects.get(Invoice_No=invoice_no)
#             serializer = OrderSerializer(order, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Orders.DoesNotExist:
#             return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)










# @api_view(['POST'])
# def addCustomerOrder(request, cid):
#     try:
#         # Get the customer object based on the cid
#         customer = Customer.objects.get(Customer_id=cid)
#     except Customer.DoesNotExist:
#         return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

#     # Add the customer instance to the request data
#     request.data['customer'] = cid
    
#     # Create the order serializer instance
#     serializer = OrderSerializer(data=request.data)

#     # Validate and save the order
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def getOrder(request,cid):

#     customer = Customer.objects.get(Customer_id=cid)
 
#     orders = Orders.objects.filter(Customer_id=customer)
    
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)


# class OrderItemDetail(APIView):
#     def post(self, request, c_id, format=None):
#         try:
#             customer = Customer.objects.get(Customer_id=c_id)
#         except Customer.DoesNotExist:
#             return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

#         try:
#             order = Orders.objects.get(Order_id=request.data.get('Invoice_No'))
#             if order.Customer_id != customer:
#                 return Response({'error': 'Order does not belong to the specified customer'}, status=status.HTTP_400_BAD_REQUEST)
#         except Orders.DoesNotExist:
#             return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = OrderItemsSerializer(data=request.data, context={'customer_id': c_id})

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, c_id, format=None):
#         try:
#             customer = Customer.objects.get(Customer_id=c_id)
#             orders = Orders.objects.filter(Customer_id=customer)
#             order_items = OrderItems.objects.filter(Invoice_No__in=orders)
#             serializer = OrderItemsSerializer(order_items, many=True)
#             return Response(serializer.data)
#         except Customer.DoesNotExist:
#             return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class OrderItemDetail(APIView):
#     def post(self, request, c_id, format=None):
#         try:
#             customer = Customer.objects.get(Customer_id=c_id)
#         except Customer.DoesNotExist:
#             return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

#         try:
#             order = Orders.objects.get(Invoice_No=request.data.get('Invoice_No'))
#             if order.Customer_id != customer:
#                 return Response({'error': 'Order does not belong to the specified customer'}, status=status.HTTP_400_BAD_REQUEST)
#         except Orders.DoesNotExist:
#             return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = OrderItemsSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, c_id, format=None):
#         try:
#             customer = Customer.objects.get(Customer_id=c_id)
#             orders = Orders.objects.filter(Customer_id=customer)
#             order_items = OrderItems.objects.filter(Invoice_No__in=orders)
#             serializer = OrderItemsSerializer(order_items, many=True)
#             return Response(serializer.data)
#         except Customer.DoesNotExist:
#             return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class OrderItemDetail(APIView):
#     def post(self, request, invoice_no, format=None):
#         try:
#             order = Orders.objects.get(Invoice_No=invoice_no)
#         except Orders.DoesNotExist:
#             return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = OrderItemsSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save(Invoice_No=order)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, invoice_no, format=None):
#         try:
#             order = Orders.objects.get(Invoice_No=invoice_no)
#             order_items = OrderItems.objects.filter(Invoice_No=order)
#             serializer = OrderItemsSerializer(order_items, many=True)
#             return Response(serializer.data)
#         except Orders.DoesNotExist:
#             return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)























# @api_view(['POST'])
# def create_order_item(request, c_id):
#     try:
#         customer = Customer.objects.get(Customer_id=c_id)
#     except Customer.DoesNotExist:
#         return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

#     try:
#         order = Orders.objects.get(Order_id=request.data.get('order_id'))
#         if order.Customer_id != customer:
#             return Response({'error': 'Order does not belong to the specified customer'}, status=status.HTTP_400_BAD_REQUEST)
#     except Orders.DoesNotExist:
#         return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

#     serializer = OrderItemsSerializer(data=request.data, context={'customer_id': c_id})

#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def getOrderData(request, cid):
#     try:

#         customer = Customer.objects.get(Customer_id=cid)

#         orders = Orders.objects.filter(Customer_id=customer)

#         order_items = OrderItems.objects.filter(order_id__in=orders)
        

#         serializer = OrderItemsSerializer(order_items, many=True)
        
#         return Response(serializer.data)
#     except Customer.DoesNotExist:
#         return Response({"error": "Customer not found"}, status=404)
#     except Exception as e:
#         return Response({"error": str(e)}, status=500)




# try:
#         companies = Company.objects.get(name=org_name)
#         customer = Customer.objects.filter(company=companies.id)
#         serializer = CustomerSerializer(customer, many=True)
#         return Response(serializer.data)
#     except Customer.DoesNotExist:
#         raise Http404("Customer does not exist")


# from django.shortcuts import get_object_or_404

# @api_view(['POST'])
# def addCustomer(request, org_name):

#     company = get_object_or_404(Company, name=org_name)
    

#     data = request.data.copy()
#     data['company'] = company.id


#     serializer = CustomerSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     else:
#         return Response(serializer.errors, status=400)
    

# @api_view(['GET'])
# def getCustomerData(request, org_name):
#     try:
#         companies = Company.objects.get(name=org_name)
#         customer = Customer.objects.filter(company=companies.id)
#         serializer = CustomerSerializer(customer, many=True)
#         return Response(serializer.data)
#     except Customer.DoesNotExist:
#         raise Http404("Customer does not exist")



# class OrderUpdateAPIView(APIView):
#     def put(self, request, invoice_no, format=None):
#         try:
#             order = Orders.objects.get(Invoice_No=invoice_no)
#         except Orders.DoesNotExist:
#             return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


#         updated_data = {
#             'Invoice_No': order.Invoice_No,
#             'status': request.data.get('status', order.status),
#             'modes_of_payment': request.data.get('modes_of_payment', order.modes_of_payment),
#             'total': request.data.get('total', order.total),
#             'vat': request.data.get('vat', order.vat),
#             'subtotal': request.data.get('subtotal', order.subtotal),
#             'Customer_id': request.data.get('Customer_id', order.Customer_id.Customer_id),
#         }


#         serializer = OrderSerializer(order, data=updated_data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)