<<<<<<< HEAD

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
=======
from django.contrib import admin
from django.urls import path
from skyhealthcheckapp import views as managerLogin
from skyhealthcheckapp import views as engineerLogin

urlpatterns = [
 path('admin/', admin.site.urls),
 path('managerlogin/',managerLogin.managementLogin),
 path('engineerlogin/',engineerLogin.engineerLogin),
 
>>>>>>> d57c08ac77be916ae7cd3a8afbc52b627a76a7f9
]
