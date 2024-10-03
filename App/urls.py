from django.urls import path,include
from .views import *


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('payment_method', Payment_methodViewSet,basename='Payment_method')
router.register('tax', TaxViewSet,basename='Tax')
router.register('role',RoleViewSet,basename='Role')

urlpatterns = [
    path('',include(router.urls)),
    path('signup/',SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/',Logout.as_view()),
    path('company_details/',CompanyDetailsAPI.as_view()),
    path('customer/',CustomerAPI.as_view()),
    path('product/',ProductAPI.as_view()),
    path('invoice/',InvoiceAPI.as_view()),
    path('invoice_item/',Invoice_itemAPI.as_view()),
    # path('item_tax/',ItemTax.as_view()),
    path('payment/',PaymentAPIView.as_view()),
    # path('in/',invoice_invoice_item),
    # path('invoices/', PDFView.as_view())
] 





