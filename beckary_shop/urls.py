from django.urls import path
from django.conf.urls.static import static

from mybeckary import settings
from . import views

app_name='beckary_shop'

urlpatterns = [
    path('', views.sec_list, name='sec_list'),
    path('<slug:slug>/', views.cat_list, name='cat_list'),
    path('<slug:sec_slug>/<slug:cat_slug>/', views.prod_list, name='prod_list'),
    path('<slug:sec_slug>/<slug:cat_slug>/<slug:prod_slug>/', views.prod_detail, name='prod_detail'),
    #path('<slug:slug>', views.prod_detail, name='prod_detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)