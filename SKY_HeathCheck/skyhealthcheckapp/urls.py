from django.contrib import admin
from django.urls import path
from skyhealthcheckapp import views as managerLogin
from skyhealthcheckapp import views as engineerLogin

urlpatterns = [
 path('admin/', admin.site.urls),
 path('managerlogin/',managerLogin.managementLogin),
 path('engineerlogin/',engineerLogin.engineerLogin),
 
]
