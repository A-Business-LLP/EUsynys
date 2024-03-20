from .serializers import RegionTablesSerializer, TableSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics
from .models import CustomUser, Table
from rest_framework import status
from rest_framework.exceptions import PermissionDenied


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
