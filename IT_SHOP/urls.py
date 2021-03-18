"""IT_SHOP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from IT_SHOP import settings
from online_shop import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path(r"accounts/", include("django.contrib.auth.urls")),
                  path('logout/', views.logout_shortcut,name='logout_shortcut'),
                  path('signup/', views.signup, name='signup'),
                  path(r'', RedirectView.as_view(url='shop/home')),
                  path(r"shop/", include("online_shop.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
