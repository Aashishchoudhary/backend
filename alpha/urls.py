from django.urls import path
from .views import *


urlpatterns= [
    path('add-library/' , AddLibrary.as_view()),
    path('add-seat/<int:id>/' , AddSeat.as_view()),
    path('library-view/<int:id>/' , LibraryView.as_view()),
    path('view-seat/<int:id>/' , LibSeatView.as_view()),
    path('view-seat/<int:lib_id>/<int:id>/' , SeatResView.as_view()),
    path('previous-student/<int:id>/' , PreviousUser.as_view()),
    path('previous-student/<int:id>/<int:idt>/' , PreviousStu.as_view()),
    path('half-day-student/<int:id>/' , HalfTimerView.as_view()),
    path('extra-student/<int:id>/' , ExtraTimerView.as_view()),
    path('half-day-student-view/<int:id>/',HalfTimerDelte.as_view()),
    path('extra-student-view/<int:id>/' , ExtraStudentDelte.as_view()),
    path("library-view/" , LibView.as_view()),
    path('all-seat-reservation-view/<int:id>/',allReservation.as_view()),
    path('edit-reservation-view/<int:id>/' , AddRes.as_view()),
    # path('total-collection/' , total_amount_labraries.as_view()),
    # path('total-collection/<int:id>/' , TotalAmount_library_wise.as_view()),
    path('payment-view/' ,paymentViewPriceDiscoveryModel.as_view()),
    # path('total/<int:id>/<int:idt>/' , IndiAmountView.as_view()),
     path('total/<int:id>/' , TotalAmount.as_view()),
    path('total/<int:id>/<int:idt>/' , IndiAmountView.as_view()),
    

]