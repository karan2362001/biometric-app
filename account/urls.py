from django.urls import path
from . import views
from account.views import UserRegistrationView, UserLoginView, UserLogoutView

urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("signin/",views.signin,name="signin"),
    path("signup/",views.signup,name="signup"),
    path('logout/',views.logout,name="logout"),
    path('api/auth/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/auth/login/', UserLoginView.as_view(), name='user-login'),
    path('api/auth/logout/', UserLogoutView.as_view(), name='user-logout'),
]