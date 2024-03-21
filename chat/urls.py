from django.urls import path
from .views import *




urlpatterns=[
    path('create-signature/' , sign_genration.as_view()),
    path('chat-page/' , chat_message.as_view()),
    path('chat-page/add-reservation-data/<int:lib_id>/<int:id>/<int:user_id>/<str:sign>/' , add_seat_reservation_view.as_view()),
    path('half-chat-page/' , half_chat_message.as_view()),
    path('half-chat-page/add-half-time/<int:id>/<int:user_id>/<str:sign>/' ,half_time_add.as_view()),
    path('half-chat-page/add-extra-time/<int:id>/<int:user_id>/<str:sign>/' ,add_extra.as_view())
  
]