from rest_framework import serializers

from .models import Company, CompanyType, Department, Employee, News, Request, RequestImage


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "image", "first_name", "last_name", "role", "phone_number", "region", "district", "password", "passport", "image", "department"]

    def create(self, validated_data):
        employee: Employee = super().create(validated_data)
        employee.is_active = True
        employee.set_password(validated_data["password"])
        employee.save()

        return employee

    def update(self, instance, validated_data):
        password = validated_data.get("password")

        employee: Employee = super().update(instance, validated_data)

        if password:
            employee.set_password(password)
            employee.save()

        return employee


class CompanyTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyType
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ["id", "name", "stir", "status", "region", "district", "phone_number", "company_type", "department"]

    def to_representation(self, instance: Company):
        data = super().to_representation(instance)

        data["department"] = DepartmentSerializer(instance.department).data
        data["company_type"] = CompanyTypeSerializer(instance.company_type).data

        return data


class RequestSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False), write_only=True, required=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    uploader = EmployeeSerializer(read_only=True)
    performer = EmployeeSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ["id", "uploader", "performer", "company", "priority", "description", "long", "lat", "file", "images", "status"]

    def create(self, validated_data):
        images = validated_data.pop("images")
        created_request = super().create(validated_data)

        for img in images:
            RequestImage.objects.create(request=created_request, image=img)

        return created_request

    def update(self, instance, validated_data):
        images = validated_data.pop("images", [])

        if images:
            instance.images.all().delete()

            for img in images:
                RequestImage.objects.create(request=instance, image=img)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serialized_data = super().to_representation(instance)
        serialized_data["company"] = CompanySerializer(instance.company).data
        serialized_data["images"] = [self.context["request"].build_absolute_uri(img.image.url) for img in instance.images.all()]
        return serialized_data


class RequestImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestImage
        fields = ["id", "request", "image"]


class StirAuthenticationSerializer(serializers.Serializer):
    stir = serializers.CharField()


class PhoneNumberOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.IntegerField()


class NewsSerializer(serializers.ModelSerializer):
    department = serializers.IntegerField(source="department_id", read_only=True)

    class Meta:
        model = News
        fields = "__all__"
