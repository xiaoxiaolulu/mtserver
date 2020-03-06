from rest_framework import serializers
from apps.meituan.models import Merchant, GoodsCategory, Goods, UserAddress, Order


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()

    class Meta:
        model = Goods
        # fields = "__all__"
        exclude = ['category']

    def validate_category_id(self, value):
        if not GoodsCategory.objects.filter(pk=value).exists():
            raise serializers.ValidationError("分类不存在！")
        return value

    def create(self, validated_data):
        category_id = validated_data.get('category_id')
        category = GoodsCategory.objects.get(pk=category_id)
        goods = Goods.objects.create(**validated_data, category=category)
        return goods


class GoodsCategorySerializer(serializers.ModelSerializer):
    # merchant = MerchantSerializer(read_only=True)
    merchant_id = serializers.IntegerField()
    goods_list = GoodsSerializer(many=True, read_only=True)

    class Meta:
        model = GoodsCategory
        # fields = "__all__"
        exclude = ['merchant']

    def validate_merchant_id(self, value):
        if not Merchant.objects.filter(pk=value).exists():
            raise serializers.ValidationError("商家不存在！")
        return value

    def create(self, validated_data):
        merchant_id = validated_data.get('merchant_id')
        merchant = Merchant.objects.get(pk=merchant_id)
        category = GoodsCategory.objects.create(**validated_data, merchant=merchant)
        return category


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        exclude = ['user']


class CreateOrderSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    goods_id_list = serializers.ListField(min_length=1)
