
# ? aynı işlemi serializer ya da view da yapabilirdim.

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Purchases, Sales

# ! pre_save
# purchase tablosuna veri save etmeden önce price_total'i hesaplayıp öyle ekleyeceğiz bunun için pre_save kullandık.çünkü db'de (model) price_total'e null=True atamamışım bu yüzden hata verir.blank=True front-end ile alakalı birşey.formlardan boş veri geldiğinde serializer'ın validasyonundan geçer çünkü blank=True.
# db'ye kaydetmeden önce price_total fieldını eklemem gerekiyor bunun için pre_save kullanıyorum yani kaydetmeden önce hesapla öyle db'ye kaydet

# sender=Purchases (sinyali gönderen Purchases tablosu)
@receiver(pre_save, sender=Purchases)
def calculate_total_price(sender, instance, **kwargs):
    instance.price_total = instance.quantity * instance.price

@receiver(pre_save, sender=Sales)
def calculate_total_price(sender, instance, **kwargs):
    instance.price_total = instance.quantity * instance.price