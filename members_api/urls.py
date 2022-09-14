from ast import Pass
from django.urls import path
from .views import RequestPasswordReset, ProfileList, ProfileDetail, MyObtainTokenPairView, RegisterView, ResettingPassword

app_name = 'members_api'

urlpatterns = [
    path('<int:pk>/', ProfileDetail.as_view(), name='detailcreate'),
    path('', ProfileList.as_view(), name='listcreate'),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('request_password_reset/', RequestPasswordReset.as_view(), name='request_password_reset'),
    path('password_reset/<str:encoded_pk>/<str:token>/',
          ResettingPassword.as_view(),  
          name="resetting_password"  
        )
]
