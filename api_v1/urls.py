from django.urls import path
from .views import CookieTokenRefreshView, CookieTokenObtainPairView, RegionTablesView, CreateTableView

urlpatterns = [
    path("v1/token/", CookieTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("v1/token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("v1/user/region/tables/", RegionTablesView.as_view(), name="region_tables"),
    path('v1/tables/create/', CreateTableView.as_view(), name='create_table'),

]
