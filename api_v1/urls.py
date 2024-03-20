from django.urls import path
from .views import RegionTablesView, CreateTableView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path("v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("v1/user/region/tables/", RegionTablesView.as_view(), name="region_tables"),
    path('v1/tables/create/', CreateTableView.as_view(), name='create_table'),

]
