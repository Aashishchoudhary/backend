from django.urls import path
from .views import *


urlpatterns =[
    #view subscriptioin details
    path('view-subscription-details/' ,viewSubscription.as_view()),

    #type of plans
    path('get-one-month-plan/' ,paymentApi.as_view()),
    path('get-three-month-plan/' ,paymentApi_3months.as_view() ),
    # path('get-six-month-plan/' , ),
    path('pay-one-month-plan/' , addPaymentModel.as_view()),
    path('pay-three-month-plan/' ,addPaymentModel_3months.as_view() ),
    # path('pay-six-month-plan/' , ),
    path('subscribed-user-three-model/' ,subscribed_user_3months_model.as_view() ),
    path('subscribed-user-one-model/' ,subscribed_user_one_month_model.as_view()),
 
   
]