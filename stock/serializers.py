from rest_framework import serializers
from .models import Brand,Category,Firm,Product,Purchases,Sales

# category modelini listelediğimizde id ve name listelenir.başka field ekleyerek zenginleştirmek istiyorsak SerializerMethodField kullanırız.bunun ile kategori altındaki ürünleri ekleyebilirim ya da ürünlerin sayısını ekleyebilirim vs..

class CategorySerializer(serializers.ModelSerializer):

    product_count=serializers.SerializerMethodField() # read_only

    class Meta:
        model=Category
        fields=("id","name","product_count")

    def get_product_count(self,obj):
        # obj : her bir kategori
        return Product.objects.filter(category_id=obj.id).count()

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        # fields="__all__"
        # fields=("name",)
        fields=["name"]

class CategoryProductSerializer(serializers.ModelSerializer):

    product_count=serializers.SerializerMethodField() # read_only
    category_products=ProductSerializer(many=True)

    class Meta:
        model=Category
        fields=("id","name","product_count","category_products")

    def get_product_count(self,obj):
        # obj : her bir kategori
        return Product.objects.filter(category_id=obj.id).count()

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'id',
            'name',
            'image'
        )
    
class FirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = (
            'id',
            'name',
            'phone',
            'image',
            'address'
        )
        
    





        