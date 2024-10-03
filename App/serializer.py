from rest_framework import routers, serializers,viewsets
from .models import*
from .serializer import *
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = '__all__'



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = '__all__'        
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'    
        
            
class Invoice_itemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product_id.product_name',read_only=True)
    # tax_details = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Invoice_item
        fields = '__all__'  
    
    # def get_tax_details(self, obj):
    #     item_detls = Item_tax.objects.filter(invoice_item_id=obj)
    #     return Item_taxSerializer(item_detls, many=True).data
    
                    
class InvoiceSerializer(serializers.ModelSerializer):
    invoice_item_id= Invoice_itemSerializer(read_only=True,many=True)
    customer_details = serializers.SerializerMethodField(read_only=True)
    tax_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Invoice
        # fields = '__all__'   
        fields = ['invoice_id','invoice_number','customer_details','generated_date','due_date','tax_details','tax_amount','total_amount','status','invoice_item_id','pdf'] 

    def get_tax_details(self, obj):
        item_detls = Tax.objects.filter(invoice=obj)
        return TaxSerializer(item_detls, many=True).data 
    
    
    def get_customer_details(self, obj):
        details = Customer.objects.get(customer_name=obj)
        return CustomerSerializer(details).data 
       
             
class Payment_methodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment_method
        fields = '__all__'

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'     
        
class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'        
        
# class Item_taxSerializer(serializers.ModelSerializer):
#     tax_name = serializers.CharField(source='tax.tax_name',read_only=True)
#     tax_rate = serializers.CharField(source='tax.rate',read_only=True)
#     class Meta:
#         model = Item_tax
#         fields = '__all__'      
# 
#   

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'