from django.shortcuts import render

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .serializers import CookieTokenRefreshSerializer, RegionTablesSerializer, TableSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics
from .authentication import CookieJWTAuthentication
from .models import CustomUser, Table
from rest_framework import status
from rest_framework.exceptions import PermissionDenied


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if "access" in response.data and "refresh" in response.data:
            access_cookie_max_age = 3600  # 1 hour
            refresh_cookie_max_age = 3600 * 24 * 1  # 1 day

            response.set_cookie(
                "access_token",
                response.data["access"],
                max_age=access_cookie_max_age,
                httponly=True,
            )
            del response.data["access"]

            response.set_cookie(
                "refresh_token",
                response.data["refresh"],
                max_age=refresh_cookie_max_age,
                httponly=True,
            )
            del response.data["refresh"]

            # Устанавливаем статус ответа на 203
            response.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION

        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):    
    def finalize_response(self, request, response, *args, **kwargs):
        if "refresh" in response.data:
            cookie_max_age = 3600 * 24 * 1  # 1 day
            response.set_cookie(
                "refresh_token",
                response.data["refresh"],
                max_age=cookie_max_age,
                httponly=True,
            )
            del response.data["refresh"]

            # Устанавливаем статус ответа на 203
            response.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION

        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = CookieTokenRefreshSerializer


class RegionTablesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        # Предполагаем, что у каждого пользователя может быть только один регион
        if hasattr(user, 'regions'):
            regions = user.regions.all()
            serializer = RegionTablesSerializer(regions, many=True)
            return Response(serializer.data)
        return Response({"error": "User has no region"}, status=400)


class CreateTableView(generics.CreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Получаем регион из запроса
        region = serializer.validated_data.get('region')
        user = self.request.user
        
        # Проверяем, связан ли пользователь с регионом
        if not user.regions.filter(id=region.id).exists():
            raise PermissionDenied({'message': 'You do not have permission to create a table for this region.'})
        
        serializer.save()
