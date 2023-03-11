from django.db import models
from django.contrib.auth.models import User

# ! Abstract Class
# classlar arasında ortak fieldlar varsa bunlar tek bir class'a çekilebilir.Bu class'tan instance üretilmez.örneğin created ve update tarihleri tüm classlarda field oalrak ayrı ayrı varsa bunları tek bir class'a çekebiliriz
# ? classları abstract classtan türetirken ilgili değişikliği yapıyoruz.buradaki örnekte models.Model --> UpdateandCreate çevirmesini yapıyoruz
class UpdateandCreate(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=25)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name="Category"
        verbose_name_plural="Categories"
        # model isminin admin panelde görünme ayarları
class Brand(models.Model):
    name=models.CharField(max_length=25,unique=True)
    # aynı isimde başka bir marka olmasın (unique=True)
    image=models.TextField()
    # veritabanı sağlığı açısından resimlerin linkini tutacağım,direkt kendilerini değil

    def __str__(self):
        return self.name
class Product(UpdateandCreate):
    name=models.CharField(max_length=100,unique=True)
    # bir ürün birden fazla kez olmasın
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category_products")
    # category tablosundan product'a ulaşmak için related name verdik.
    # ! yani sanki category tablosunun category_products(related name) isminde bir field'ı varmış gibi düşünebiliriz.
    # ? db'de category_id olarak tutulur.(relations'tan dolayı)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,related_name="brand_products")
    # ? db'de brand_id olarak tutulur.(relations'tan dolayı)
    stock=models.PositiveSmallIntegerField(blank=True,default=0)
    # üründen kaç adet oldugu bilgisi.blank=True stok bilgisi boş bırakılabilsin hata vermesin.

    def __str__(self):
        return self.name
    
    # ! Product-Category arasındaki ilişki
    # one-to-one olmaz : çünkü bir ürün sadece bir kategoriye ait olur ve o kategoriye başka ürün dahil olamaz anlamına gelir
    # one-to-many olabilir : bir ürün bir kategoriye ait olacak fakat başka ürünler de o kategoriye ait olabilir.bu projede bu relation'a göre tasarlanacak (proje tasarımına bağlı)
    # many-to-many olabilir : bir ürün hem ev eşyası hem de elektronik kategorisine girebilir.bu projede bu relations'ı kullanmayacağız.(proje tasarımına bağlı)
    # ? Relations'ları anlamak için kaynak :
    # https://teknikakil.com/veritabani/veritabani-tasarimi/veritabaninda-iliski-turleri-bire-bir-bire-cok-coka-cok/

class Firm(UpdateandCreate):
    name=models.CharField(max_length=25,unique=True)
    phone=models.CharField(max_length=25)
    address=models.CharField(max_length=200)
    image=models.TextField()

    def __str__(self):
        return self.name
class Purchases(UpdateandCreate):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    firm=models.ForeignKey(Firm,on_delete=models.SET_NULL,null=True,related_name="firm_purchases")
    brand=models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True,related_name="brand_purchases")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_purchases")
    # related fieldlar db'ye _id eklemesiyle kaydedilir
    # örnek product-> product_id şeklinde kayıt edilir.
    quantity=models.PositiveSmallIntegerField()
    price=models.DecimalField(max_digits=6,decimal_places=2)
    # decimal : virgüllü sayılar olabilir
    # decimal_places : virgülden sonra kaç hane gözükeceği
    price_total=models.DecimalField(max_digits=8,decimal_places=2,blank=True)
   
    def __str__(self):
        return f'{self.product} - {self.quantity}'
class Sales(UpdateandCreate):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    brand=models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True,related_name="brand_sales")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_sales")
    quantity=models.PositiveSmallIntegerField()
    price=models.DecimalField(max_digits=6,decimal_places=2)
    # decimal : virgüllü sayılar olabilir
    # decimal_places : virgülden sonra kaç hane gözükeceği
    price_total=models.DecimalField(max_digits=8,decimal_places=2,blank=True)
   
    def __str__(self):
        return f'{self.product} - {self.quantity}'


