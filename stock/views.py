from django.shortcuts import render
from rest_framework import viewsets,filters,status
from .models import Brand,Category,Firm,Product,Purchases,Sales
from .serializers import CategorySerializer,CategoryProductSerializer,BrandSerializer,FirmSerializer,ProductSerializer,PurchasesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

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

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'brand']
    search_fields = ['name']

class PurchaseView(viewsets.ModelViewSet):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['firm', 'product']
    search_fields = ['firm']  

    # ! override : ModelViewSet -> CreateModelMixin -> create and perform_create methods

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # gelen veri serializers'dan geçsin
        serializer.is_valid(raise_exception=True) # serializer'ın validasyonundan da geçsin
        # ! ############ ADD PRODUCT STOCK ##################
        purchase=request.data # gelen data'yı purchase değişkenine atadım
        product=Product.objects.get(id=purchase["product_id"])
        product.stock += purchase["quantity"]
        # ilgili ürünün stok miktarını quantity kadar artırıp güncelledik. 
        product.save()
        # ! ##################################################
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # serializer.save()
        serializer.save(user=self.request.user)
        # stock artırımını hangi user'ın yaptığını kayıt ediyoruz
        # aynı işlem serializers'da create metodunu override ederek de yapılabilir,fakat bu yöntem daha kolay.