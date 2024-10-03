from django.contrib import admin
from .models import *



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = Customer.DisplayField
    
@admin.register(CoreUser)
class CoreUserAdmin(admin.ModelAdmin):
    list_display = CoreUser.DisplayField
    # list_editable = ('email','contact')

@admin.register(CompanyDetails)
class CompanyDetailsAdmin(admin.ModelAdmin):
    list_display = CompanyDetails.DisplayField

@admin.register(Payment_method)
class Payment_mthodAdmin(admin.ModelAdmin):
    list_display = Payment_method.DisplayField

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = Tax.DisplayField

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = Invoice.DisplayField
    list_editable=['generated_date']
    
@admin.register(Invoice_item)
class Invoice_itemAdmin(admin.ModelAdmin):
    list_display = Invoice_item.DisplayField

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = Product.DisplayField

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = Payment.DisplayField
    
# @admin.register(Item_tax)
# class Item_taxAdmin(admin.ModelAdmin):
#     list_display = Item_tax.DisplayField

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display=Role.DisplayField