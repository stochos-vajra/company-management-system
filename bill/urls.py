from django.urls import path, include


# from .views import getProductData, getCompanyData, addCompany, addProductData,addCategoryData, getCategoryData, addCompany_Type, getCompany_Type, getCustomerData

 
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()



urlpatterns = [

    path('company_type/', CompanyTypeListCreate.as_view(), name='company_type_list_create'),

    path('Company/', CompanyListCreate.as_view(), name='company_list_create'),
    path('Company/<str:org_name>/', CompanyListCreate.as_view(), name='company_detail'),

    path('Product/<str:org_name>/', ProductDataListCreate.as_view(), name='product_data_list_create'),

    path('Category/<str:org_name>/', CategoryDataListCreate.as_view(), name='category_data_list_create_by_org_name'),

    path('Customer/<str:org_name>/', CustomerDataListCreate.as_view(), name='customer_data_list_create'),
   
    path('customer/<str:cid>/order/', CustomerOrderDetail.as_view(), name='customer_order_detail'),

    path('customer/<str:invoice_no>/order/items/', OrderItemDetail.as_view(), name='order_item_detail'),

    path('Orders/<str:org_name>/', OrdersDataListCreate.as_view(), name='customer_data_list_create'),
    path("show/",show),

    path("home/",home)




    


    
]



    # company_types
    # path("getCompanyType/",getCompany_Type, name="getCompanyType"),
    # path("addCompanyType/",addCompany_Type, name="addCompanyType"),


        # line 27 and 28 company data 

    # path("addCompany/",addCompany,name="addCompany"),
    # path("Company/<str:org_name>/",getCompanyData, name="Company"),


        # line 33 and 34 product datas
    # path("Product/<str:org_name>/",getProductData, name="getProduct"),
    # path("addProduct/<str:org_name>/",addProductData, name="addProduct"),

     #  line 38 39 category belonging to company
    
    # path("Category/<str:org_name>/",getCategoryData, name="getCategory"),
    # path("addCategory/",addCategoryData, name="addCategory"),
    
    # line 43 and 44 customer data gets
    
    # path("Customer/<str:org_name>/",addCustomer, name="Customer"),
    # path("getCustomer/<str:org_name>/",getCustomerData, name="getCustomer"),

    # line 49 and 50 get customer order 

    # path("Customerorder/<str:cid>/",getOrder,name="Customerorder"),
    # path("addOrder/<str:cid>/",addCustomerOrder,name="addOrder"),


    # line 49 and 50 get customer order 

    # path("Customerorder/<str:cid>/",getOrder,name="Customerorder"),
    # path("addOrder/<str:cid>/",addCustomerOrder,name="addOrder"),

    # # line 54 and 55 add product based on customer order
#     path("postOrder/<str:c_id>/",create_order_item,name="postOrder"),
#     path("getOrders/<str:cid>/",getOrderData,name="getOrders"),
