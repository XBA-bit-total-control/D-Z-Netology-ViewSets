from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    title = models.CharField(
        max_length=60,
        unique=True,
        verbose_name="Наименование"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["id", "title"]

    def __str__(self):
        return f"{self.title}"


class Stock(models.Model):
    address = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Адрес"
    )
    products = models.ManyToManyField(
        Product,
        through='StockProduct',
        related_name='stocks',
        verbose_name="Продукты"
    )

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"
        ordering = ["id", "address"]

    def __str__(self):
        return f"{self.address}"


class StockProduct(models.Model):
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name='positions',
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='positions',
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        verbose_name = "Связующее звено"
        verbose_name_plural = "Связующее звено"

    def __str__(self):
        return f"{self.stock} : {self.product} : {self.quantity} : {self.price}"
