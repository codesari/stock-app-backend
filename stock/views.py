from django.shortcuts import render
from rest_framework import viewsets,filters
from .models import Brand,Category,Firm,Product,Purchases,Sales
from .serializers import CategorySerializer,CategoryProductSerializer,BrandSerializer,FirmSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions

class CategoryView(viewsets.ModelViewSet):

    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['name']
    #  http://127.0.0.1:8000/stock/categories/?search=
    filterset_fields=['name']
    #  http://127.0.0.1:8000/stock/categories/?search=&name=
    #  http://127.0.0.1:8000/stock/categories/?search=&name=Elektronik
    permission_classes=[DjangoModelPermissions]

    # serializer seçmeye yarayan metod
    def get_serializer_class(self):
        if self.request.query_params.get("name"):
        #  query_params : endpointteki query keywordlerini yakalar
        # eger ..?search=&name=Elektronik gibi girilen bir endpointse CategoryProductSerializers'ı seç
            return CategoryProductSerializer
        # değilse normal,yukarıda belirtilen serializer'ı seç
        return super().get_serializer_class()
    
class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class FirmView(viewsets.ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
