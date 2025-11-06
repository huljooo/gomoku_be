from rest_framework import serializers
from .models import Person, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'person']

class PersonSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = ['id', 'name', 'surname', 'age', 'hobby', 'addresses']