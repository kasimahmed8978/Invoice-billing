from rest_framework.response import Response
from .models import * 
from .serializer import *
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import response
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser , JSONParser,FormParser
import json
# from rest_framework.pagination import PageNumberPagination
 

class SignUpView(APIView):
    
        def post(self,request):
            validate_data = request.data
            # print('\n\n\n',validate_data,'\n\n\n')
            role_name = validate_data['role']
            role_object=Role.objects.get(role_id=role_name)
            
            user_data = {
                'user_name': validate_data.get('user_name'),
                'role': role_object
            }
            # print('\n\n\n\n',user_data,'\n\n\n\n')

            serializer=SignUpSerializer(data=validate_data)
            if serializer.is_valid():
                user = CoreUser.objects.create(**user_data)
                user.set_password(validate_data.get('password'))
                user.save()
                return Response(
                            {"message":"User Registered Successfully"}
                       )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









        # def post(self, request):
        #     validate_data = request.data
        #     role = CoreUser.role.role_type
        #     role_name = validate_data.get('role')  

        #     try:
        #         role_object,new = Role.objects.get_or_create(role_type=role)
        #     except Role.DoesNotExist:
        #         return Response({'error': 'Role not found'}, status=status.HTTP_400_BAD_REQUEST)
            
        #     serializer=SignUpSerializer(data=validate_data)
        #     if serializer.is_valid():
        #         user = CoreUser(
        #             username=validate_data['user_name'],
        #             role=role_object
        #         )
        #         user = CoreUser.objects.create(**user)
        #         user.set_password(validate_data['password'])  # Hash the password
        #         user.save()

        #         return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)

        

class LoginView(APIView):

    def post(self,request):
        try:
            data = request.data 
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                try:
                    username = serializer.data['username']
                    password = serializer.data['password']
                    user = authenticate(username=username,password=password)
                    if user is None:
                        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token
                    custom_claims = access_token.get('custom_claims', {})
                    # custom_claims['user_id'] = user.user_id
                    # custom_claims['first_name'] = user.first_name
                    # custom_claims['last_name'] = user.last_name
                    # access_token['custom_claims'] = custom_claims
                    print({'refresh': str(refresh),
                        'access': str(access_token)})
                    return Response({
                        'refresh': str(refresh),
                        'access': str(access_token),
                        # 'user': custom_claims
                    }) 
                except Exception as e:
                    return Response({"error": f"Error during authentication: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
                  
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
              
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 



class Logout(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print('\n\n\n',request.data,'\n\n\n')
        
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"Message":"Enter refresh_token"})
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":"Success"},
                            status=status.HTTP_200_OK
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
        


        

class CompanyDetailsAPI(APIView):
    parser_classes = [MultiPartParser]
    def get(self,request):
        try:
            c_d_obj = CompanyDetails.objects.all()
            c_d_serializer = CompanyDetailsSerializer(c_d_obj,many=True,context={"request":request})
            return Response(c_d_serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def post(self,request):
        
        try:
            validated_data = request.data
 
            c_d_data = {
                'company_name': validated_data.get('company_name'),
                'company_contact':f'+91{validated_data.get("company_contact")}',
                'company_email':validated_data.get("company_email"),
                'house_no':validated_data.get('house_no'),
                'area':validated_data.get('area'),
                'landmark':validated_data.get('landmark'),
                'pincode':validated_data.get('pincode'),
                'city':validated_data.get('city'),
                'state':validated_data.get('state'),
                'country':validated_data.get('country'),
                'bank_name': validated_data.get('bank_name'),
                'branch_name': validated_data.get('branch_name'),
                'account_number': validated_data.get('account_number'),
                'ifsc_code': validated_data.get('ifsc_code'),
                'gst_in': validated_data.get('gst_in'),
                'inv_num_format':validated_data.get('inv_num_format'),
                'company_logo': validated_data.get('company_logo'),
                'digital_seal': validated_data.get('digital_seal'),
                'digital_signature': validated_data.get('digital_signature'),
                'show_bank_data':validated_data.get('show_bank_data')
            }
            c_d_serializers = CompanyDetailsSerializer(data=validated_data)
            user_obj=CoreUser.objects.get(user_id=validated_data.get('user_id'))

            if c_d_serializers.is_valid():
                try:
                    c_d_obj = CompanyDetails.objects.create(user_id=user_obj,**c_d_data)
                    c_d_obj.save()
                    

                except Exception as e:
                    return Response({"Message": f"Error creating company details: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response({"Message":"Company Details created successfully"}, status=status.HTTP_201_CREATED)
            
            return Response(c_d_serializers.errors, status=status.HTTP_400_BAD_REQUEST) 
         
        except Exception as e:
            return Response({"Message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    

    
    def patch(self,request):
        try:
            validated_data=request.data
            company_d_upd = request.GET.get('company_d_upd')
            print('\n\n\n\n',company_d_upd,'\n\n\n\n')
            c_d_obj = CompanyDetails.objects.get(company_details_id=company_d_upd)
            try:    
                c_d_serializer = CompanyDetailsSerializer(c_d_obj,data=validated_data,partial=True)
                # print('\n\n\n\n',c_d_serializer,'\n\n\n\n\n')

                if c_d_serializer.is_valid():
                    c_d_serializer.save()
                    return Response({"Message":"Data updated successfully"}, status=status.HTTP_200_OK)

                return Response(c_d_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

            except Exception as e:
                 return Response({"Message": f"Error updating client data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except CompanyDetails.DoesNotExist:
            return Response({"Message": "CompanyDetails not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"Message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def delete(self,request):
        try:
            delete = request.GET.get('delete')
            
            if not delete:
                return Response({"Message": "company_details_id not provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                c_d_obj = CompanyDetails.objects.get(company_details_id=delete)

            except CompanyDetails.DoesNotExist:
                return Response({"Message": "CompanyDetails not found"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                c_d_obj.delete()

            except Exception as e:
                return Response({"Message": f"Error deleting CompanyDetails: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({"Message":"CompanyDetails deleted successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"Message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerAPI(APIView):
    def get(self,request):
        try:
            customer_obj = Customer.objects.all()
            customer_serializer = CustomerSerializer(customer_obj,many=True)
            return Response(customer_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self,request):
        try:
            validated_data = request.data
            print('\n\n\n',validated_data,'\n\n\n')
            
            # client_data = {
            #     'customer_name': validated_data.get('customer_name'),
            #     'house_no': validated_data.get('house_no'),
            #     'area': validated_data.get('area'),
            #     'landmark': validated_data.get('landmark'),
            #     'pincode': validated_data.get('pincode'),
            #     'city':validated_data.get("city"),
            #     'state':validated_data.get('state'),
            #     'country':validated_data('country'),
            #     'email':validated_data('email'),
            #     'phone':f'+91{validated_data.get("phone")}',
               
            # }
            customer_serializer = CustomerSerializer(data=validated_data)
            print('\n\n\n',"client data",validated_data,'\n\n\n')

            if customer_serializer.is_valid():
                try:
                    customer_obj = Customer.objects.create( 
                        customer_name=validated_data['customer_name'],
                        house_no=validated_data['house_no'],
                        area = validated_data['area'],
                        landmark=validated_data['landmark'],
                        pincode=validated_data['pincode'],
                        city=validated_data['city'],
                        state=validated_data['state'],
                        country=validated_data['country'],
                        email=validated_data['email'],
                        phone=validated_data['phone'],

                    )
                    customer_obj.save()

                    # email = customer_obj['email']
                    # message = EmailMessage(
                    #     'Test email subject',
                    #     'test email body,  client create successfully ',
                    #     settings.EMAIL_HOST_USER,
                    #     [email]
                    # )
                    # message.send(fail_silently=False)

                except Exception as e:
                    return Response({"Message": f"Error creating client: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response({"Message":"Client Registered successfully"}, status=status.HTTP_201_CREATED)
            
            return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
         
        except Exception as e:
            return Response({"Message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    

    
    def patch(self,request):
        try:
            validated_data=request.data
            customer_update = request.GET.get('customer_update')
            customer_obj = Customer.objects.get(customer_id=customer_update)
            try:    
                customer_serializer = CustomerSerializer(customer_obj,data=validated_data,partial=True)
                
                if customer_serializer.is_valid():
                    customer_serializer.save()
                    return Response({"Message":"Data updated successfully"}, status=status.HTTP_200_OK)
                
                return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
             
            except Exception as e:
                return Response({"Message": f"Error updating client data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Customer.DoesNotExist:
            return Response({"Message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"Message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def delete(self,request):
        try:
            delete_customer = request.GET.get('delete_client')
            
            if not delete_customer:
                return Response({"Message": "Customer ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                customer_obj = Customer.objects.get(customer_id=delete_customer)

            except Customer.DoesNotExist:
                return Response({"Message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                customer_obj.delete()

            except Exception as e:
                return Response({"Message": f"Error deleting customer: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({"Message":"Customer deleted successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"Message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class ProductAPI(APIView):
    def get(self,request):
        try:
            product_obj = Product.objects.all()
            product_serializer = ProductSerializer(product_obj,many=True)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request):
        try:
            validated_data = request.data
            serializer_obj = ProductSerializer(data=validated_data)
            if serializer_obj.is_valid():
                product_obj = Product.objects.create( 
                                                     product_name = validated_data["product_name"],
                                                     description=validated_data["description"],
                                                     price = validated_data["price"],
                                                     stock_quantity = validated_data["stock_quantity"],
                                                        )
                product_obj.save()
                    
                return Response({"Message":"product created successfully","Data":serializer_obj.data}, status=status.HTTP_201_CREATED)
            
            else:
                return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request):
        try:
            validated_data = request.data
            try:
                product_obj = Product.objects.get(product_id=validated_data['product_id'])

            except Product.DoesNotExist:
                return Response({"message": "product not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer_obj = ProductSerializer(product_obj, data=validated_data, partial=True)
            if serializer_obj.is_valid():
                serializer_obj.save()
                return Response({"Message": "product updated successfully"})
            else:
                return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

    def delete(self,request):
        try:
            delete = request.GET.get('delete')
            if delete:
                try:
                    product_obj = Product.objects.get(product_id=delete)
                    product_obj.delete()
                    return Response({"message": "product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
                
                except Product.DoesNotExist:
                    return Response({"message": "product not found"}, status=status.HTTP_404_NOT_FOUND)
                
            else:
                return Response({"message": "No product ID provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        

# @api_view(['GET','POST'])
# def invoice_invoice_item(request):
#      if request.method == 'GET':
#             product_obj = Invoice.objects.all()
#             product_serializer = InvoiceSerializer(product_obj,many=True)
#             print(product_serializer)
#             # l=[]
#             # for p in product_serializer:
#             #     d = p.__dict__
#             #     del(d['_state'])
#             #     l.append(d)
#             # print(l)

#             # for i in l:
#             #     print(i['invoice_number'],)

#             # return Response(product_serializer.data, status=status.HTTP_200_OK)
#             return Response({"helo":'one'})


class InvoiceAPI(APIView):
    parser_classes = [MultiPartParser,FormParser]


    def get(self,request):
        try:
            invoice_obj = Invoice.objects.all()
            # paginator = PageNumberPagination()
            # pagination_data = paginator.paginate_queryset(invoice_obj,request)
            invoice_serializer = InvoiceSerializer(invoice_obj,many=True)
            return Response(invoice_serializer.data, status=status.HTTP_200_OK)
            # return paginator.get_paginated_response(invoice_serializer.data)
        except Exception as e:
            return Response({"error":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
      try:

          validated_data = request.data.get('obj')

          if validated_data:
              # Parse the JSON string into a Python dictionary
              validated_data = json.loads(validated_data)
              print('\n\n\n','valid',validated_data,'\n\n\n')

              customer_id = validated_data['customer']
              cus = Customer.objects.get(customer_id=customer_id)
              cus_email = cus.email
              print(cus_email)

              # The provided invoice dictionary
              invoice_data = {
                  'invoice_number': validated_data.get('invoice_number'),
                  'generated_date': validated_data.get('generated_date'),
                  'due_date': validated_data.get('due_date'),
                  'customer': validated_data.get('customer'),
                  'total_amount': validated_data.get('total_amount'),
                  'status': validated_data.get('status'),
                  'tax_amount': validated_data.get('tax_amount')
              
              }
              
              try:
                  customer_obj = Customer.objects.get(customer_id=validated_data['customer']) 

              except Customer.DoesNotExist:
                return Response({"Message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

              
              tax_details = validated_data.get('tax_details', [])
              invoice_items = validated_data.get('invoice_item', [])
              
 
          invoice_pdf = request.FILES.get('pdf')
        #   print(pdf_file)
          if invoice_pdf:
 
            invoice_obj = Invoice.objects.create(
                                                    invoice_number = validated_data['invoice_number'],
                                                    customer=customer_obj,
                                                    generated_date = validated_data['generated_date'],
                                                    due_date = validated_data['due_date'],
                                                    tax_amount =validated_data['tax_amount'],
                                                    total_amount=validated_data['total_amount'],
                                                    status=validated_data['status'],
                                                    pdf = invoice_pdf
                                                    )
            
            for inv_item in invoice_items:
                product_obj = Product.objects.get(product_id=inv_item['product_id'])
                unit_price_obj = product_obj.price
                item_obj = Invoice_item.objects.create(
                                                    product_id=product_obj,
                                                    quantity=inv_item['quantity'],
                                                    unit_price=unit_price_obj,
                                                    taxable_value=inv_item['taxable_value'],
                                                    calculated_amount=inv_item['calculated_amount']
                                                    
                )
                invoice_obj.invoice_item_id.add(item_obj)
                 
                product = Product.objects.get(product_id=inv_item['product_id'])

                if product.stock_quantity >= int(inv_item['quantity']):
             
                    product.stock_quantity=product.stock_quantity -int(inv_item['quantity'])
                    product.save()
                    
            
                for tax_data in tax_details:
                    item_tax_obj, created  =Tax.objects.get_or_create(tax_id=tax_data['tax_id']) 
                    invoice_obj.tax.add(item_tax_obj)
                
                invoice_obj.save()
                print('\n\n\n','post','\n\n\n')



                email = cus_email
                invoice_pdf.seek(0)
                pdf_content = invoice_pdf.read()
                # message = EmailMessage(
                #         'Subject',
                #         'Bill from Affucent',
                #         settings.EMAIL_HOST_USER,
                #         [email]
                #     )


                message = EmailMessage(
                    subject='Bill from Affucent',
                    body='Invoice Attached Below -',
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email],
                    headers={
                        'SMS': 'Your custom SMS header'   
                    }
                )

                message.attach("invoice_pdf.pdf", pdf_content, "invoice/pdf")
                message.send(fail_silently=False)
            
           
          return Response({"message": "Data processed successfully"}, status=status.HTTP_200_OK)
      
      except json.JSONDecodeError:
          return Response({"error": "Invalid JSON format in 'obj' data"}, status=status.HTTP_400_BAD_REQUEST)
      
      except Exception as e:
          return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 
    


    def put(self,request):
        try:
            validated_data = request.data

            try:
                invoice_obj = Invoice.objects.get(invoice_id=validated_data['invoice_id'])

            except Invoice.DoesNotExist:
                return Response({"Message": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
            
            invoice_serializer = InvoiceSerializer(invoice_obj,data=validated_data,partial=True)

            if invoice_serializer.is_valid():
                invoice_serializer.save()

                if 'invoice_item_id' in validated_data:
                    invoice_obj.invoice_item_id.clear()

                    for inv_item in validated_data.get("invoice_item_id", []):
                        print('\n\n\n\n',inv_item,'\n\n\n\n\n')
                        obj, created = Invoice_item.objects.get_or_create(invoice_item_id=inv_item)
                        invoice_obj.invoice_item_id.add(obj)

                return Response({"Message":"Updated successfully"}, status=status.HTTP_200_OK )
            
            else:
                return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
             
        except Exception as e:
            return Response({"Message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self,request):
        try:
            delete = request.GET.get('delete')

            if delete:
                try:
                    invoice_obj = Invoice.objects.get(invoice_id=delete)
                    invoice_obj.delete()
                    return Response({"Message":"data deleted successfully "}, status=status.HTTP_200_OK)
                
                except Invoice.DoesNotExist:
                    return Response({"Message": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
                
            else:
                return Response({"Message": "No invoice ID provided"}, status=status.HTTP_400_BAD_REQUEST)  
            
        except Exception as e:  
            return Response({"Message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 











        
              
class Invoice_itemAPI(APIView):
    def get(self,request):
        try:
            client_obj = Invoice_item.objects.all()
            client_serializer = Invoice_itemSerializer(client_obj,many=True)
            return Response(client_serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self,request):
        try:
            validated_data = request.data
            print('\n\n\n',validated_data,'\n\n\n')
            invoiceitem_serializer = Invoice_itemSerializer(data=validated_data)

            if invoiceitem_serializer.is_valid():
               invoiceitem_serializer.save()
               return Response({"Message":"data posted successfully"}, status=status.HTTP_201_CREATED)
            
            else:
                return Response(invoiceitem_serializer._errors, status=status.HTTP_400_BAD_REQUEST) 
             
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self,request):
        try:
            validated_data = request.data
            print('\n\n\n',validated_data,'\n\n\n')
            try:
                invoiceitem_obj = Invoice_item.objects.get(invoice_item_id=validated_data['invoice_item_id'])

            except Invoice_item.DoesNotExist:
                return Response({"message": "Invoice item not found"}, status=status.HTTP_404_NOT_FOUND)
            
            invoiceitem_serializer = Invoice_itemSerializer(invoiceitem_obj,data=validated_data,partial=True)


            if invoiceitem_serializer.is_valid():
                invoiceitem_serializer.save()
                return Response({"Message":"data updated successfully"},status=status.HTTP_200_OK )

            else:
                return Response(invoiceitem_serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self,request):
        try:
            delete = request.GET.get('delete')
            if delete:
                try:
                    invoiceitem_obj = Invoice_item.objects.get(invoice_item_id=delete)
                    invoiceitem_obj.delete()
                    return Response({"message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
                
                except Invoice_item.DoesNotExist:
                    return Response({"message": "Invoice item not found"}, status=status.HTTP_404_NOT_FOUND)
                
            else:
                return Response({"message": "No invoice item ID provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
     
# class ItemTax(APIView):
#     def get(self,request):
#         try:
#             item = Item_tax.objects.all()
#             serializer = Item_taxSerializer(item,many=True)
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"message":f"Unexpected error:{str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#     def post(self,request):
#         try:
#             valid_data = request.data
#             serializer_obj = Item_taxSerializer(data=valid_data)
#             if serializer_obj.is_valid():
#                 serializer_obj.save()
#                 return Response({"message":"Item Tax Create Successfully","Data":serializer_obj.data},status=status.HTTP_201_CREATED)
            
#             return Response(serializer_obj.errors,status=status.HTTP_400_BAD_REQUEST)
            
#         except Exception as e:
#             return Response({"message":f"Unexpected error:{str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#     def put(self,request):
#         try:
#             valid_data = request.data
#             try:
#                 item_obj = Item_tax.objects.get(item_tax_id=valid_data['item_tax_id'])
#             except Item_tax.DoesNotExist:
#                 return Response("Object Not found",status=status.HTTP_404_NOT_FOUND)
            
#             serializer_obj = Item_taxSerializer(item_obj, data=valid_data, partial=True)
#             if serializer_obj.is_valid():
#                 serializer_obj.save()
#                 return Response({"Message":"Item Tax Updated Successfully"})
#             return Response(serializer_obj.errors,status=status.HTTP_400_BAD_REQUEST)
        
#         except Exception as e:
#             return Response({"Message":f"Unexpected error :{str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#     def delete(self,request):
#         try:
#             delete = request.GET.get('delete')

#             if delete:
#                 try:
#                     item_obj = Item_tax.objects.get(item_tax_id=delete)
#                     item_obj.delete()
#                     return Response("delete successfully ",status=status.HTTP_204_NO_CONTENT)
#                 except Item_tax.DoesNotExist:
#                     return Response({"message":"item tax no found "},status=status.HTTP_404_NOT_FOUND)
                
#             else:
#                 return Response({"message":"ID no provide"},status=status.HTTP_400_BAD_REQUEST)
            
#         except Exception as e:
#             return Response({"message":f"Unexcepted error :{str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                  
        
        
class PaymentAPIView(APIView):
    def get(self,request ):
        try:
            sort_by = request.query_params.get('sort_by')
            query = "SELECT * FROM payment"

            if sort_by == 'ascending':
                query += " ORDER BY amount"

            elif sort_by == 'descending':
                query += " ORDER BY amount DESC"

            try:
                payment_obj = Payment.objects.raw(query)
                serializer_obj = PaymentSerializer(payment_obj, many=True)
                return Response(serializer_obj.data, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({"Message": f"Error executing query: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({"Message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            validated_data = request.data
            print('\n\n\n',validated_data,'\n\n\n')
            
            x = Invoice.objects.filter(invoice_id=validated_data['invoice_id'])
            x.update(status='Paid')
            serializer_obj = PaymentSerializer(data=validated_data)
    
            if serializer_obj.is_valid():
                serializer_obj.save()
                return Response({"Message":"created payment successfully"},status=status.HTTP_201_CREATED)
            
            else:
                return Response(serializer_obj.errors,status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def put(self, request):
        try:
            validated_data = request.data
            print('\n\n\n',validated_data,'\n\n\n')
            update_payment = request.GET.get('update_payment')
            try:
                payment_obj = Payment.objects.get(payment_id=update_payment)

            except Payment.DoesNotExist:
                return Response({"message": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer_obj = PaymentSerializer(payment_obj ,data=validated_data)

            if serializer_obj.is_valid():
                serializer_obj.save()
                return Response({"Message":"Updated successfully"},status=status.HTTP_201_CREATED)

            else:
                return Response(serializer_obj.errors,status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request):
        try:
            delete = request.GET.get('delete')
            if delete:
                try:
                    payment_obj = Payment.objects.get(payment_id=delete)
                    payment_obj.delete()
                    return Response({"message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
                
                except Payment.DoesNotExist:
                    return Response({"message": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "No payment ID provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

##---------------------------------------Payment Method-----------------------------------------        
class Payment_methodViewSet(viewsets.ModelViewSet):
    queryset = Payment_method.objects.all()
    serializer_class = Payment_methodSerializer

##---------------------------------------Tax-----------------------------------------        
class TaxViewSet(viewsets.ModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer          
##---------------------------------------Tax-----------------------------------------        

class RoleViewSet(viewsets.ModelViewSet):
        queryset = Role.objects.all()
        serializer_class = RoleSerializer 




