from icecream.models import IceCream
from rest_framework import serializers


class ListIceCreamSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]
        IceCream.objects.bulk_create(result, ignore_conflicts=True)

        return result


class IceCreamSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return IceCream(**validated_data)

    class Meta:
        model = IceCream
        fields = "__all__"
        list_serializer_class = ListIceCreamSerializer
