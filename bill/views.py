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
    

def show(request):

    return render(request,"company_list.html")

def home(request):

    return render(request,"prep.html")


