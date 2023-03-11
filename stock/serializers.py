from rest_framework import serializers
from .models import Brand,Category,Firm,Product,Purchases,Sales
import datetime

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

    
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    # StringRelatedField'lar read only dir.post yaparken bu iki field kullanılamaz.onun yerine category_id ya da brand_id ile post yapılır
    brand_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    
    class Meta:
        model=Product
        fields=(
            'id',
            'category',
            'category_id',
            'brand',
            'brand_id',
            'name',
            'stock'
        )
        # stock field'ı purchase ve sales ile değişecek,buradan product ile değişmeyecek o yüzden read only yapıyoruz
        read_only_fields=('stock',)
        # ? eğer stock 0 dan büyükse sayı yerine 'mevcut' yazdıma nasıl yapılır 

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
        
class PurchasesSerializer(serializers.ModelSerializer):
    
    user = serializers.StringRelatedField() 
    firm = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    product_id = serializers.IntegerField()
    brand_id = serializers.IntegerField()
    firm_id = serializers.IntegerField()
    category = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    
    class Meta:
        model = Purchases
        fields = (
            "id",
            "user",
            "user_id",
            "category",
            "firm",
            "firm_id",
            "brand",
            "brand_id",
            "product",
            "product_id",
            "quantity",
            "price",
            "price_total",
            "time",
            "date"
        )
    # def get_category(self,obj):
    #     product=Product.objects.get(id=obj.product_id)
    #     category=Category.objects.get(id=product.category_id).name
    #     return category
    def get_category(self,obj):
        return obj.product.category.name
    def get_time(self,obj):
        return datetime.datetime.strftime(obj.created,"%H:%M:%S")
    def get_date(self,obj):
        return datetime.datetime.strftime(obj.created,"%d.%m.%y")
        



 
        