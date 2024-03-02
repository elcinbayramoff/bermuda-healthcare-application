from django.urls import path
from . import views

######
urlpatterns = [
    path('login/', views.login, name='login'),
    path('main/',views.main,name = 'main'),
    path('call-ambulance/',views.ambulance,name="ambulance"),
    path('check-sent/',views.get_sent_status,name="get_sent_status"),
    path('ambulance-callers/', views.callers, name="callers"),
    path('update-sent/<int:caller_id>/', views.update_sent, name="update_sent"),
    path('cancel-am/', views.cancel, name="cancel"),
    path('send-chat/', views.chatbot_view, name="chatbot_view"),    
    path('user-profile/',views.UserProfile,name='UserProfile'),
    path('delete-history/',views.delete_history,name='delete_history'),
]