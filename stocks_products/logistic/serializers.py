from multiprocessing.connection import address_type

from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate_title(self, title):
        if len(title) > 60:
            raise ValidationError("The name is too long / Слишком длинное название")
        return title


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = "__all__"

    def create(self, validated_data):

        positions = validated_data.pop('positions')

        stock = super().create(validated_data)

        for rec in positions:
            StockProduct(
                stock=stock,
                product=rec["product"],
                quantity=rec["quantity"],
                price=rec["price"]
            ).save()

        return stock

    def update(self, instance, validated_data):

        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        for rec in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=rec["product"],
                defaults=rec
            )

        return stock
