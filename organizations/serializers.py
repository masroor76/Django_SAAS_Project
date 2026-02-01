from rest_framework import serializers
from .models import Organization  # Adjust the import based on your project structure

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization  # Assuming Organization is a defined model
        fields = ['id', 'name', 'address', 'phone_number', 'created_at', 'updated_at']
