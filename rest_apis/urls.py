from django.urls import path
from . import views

urlpatterns = [
    path('register-user/', views.registerUser),
    path('apply-loan/', views.applyLoan),
    path('make-payment/', views.makePayment),
    path('get-statement/<int:loan_id>', views.getStatement),
]
