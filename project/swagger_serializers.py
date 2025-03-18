from rest_framework import serializers


class EmployeeIdSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    
