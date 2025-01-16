import hashlib
import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now


class Department(models.Model):
    name = models.CharField(max_length=512)

    region = models.CharField(max_length=128)
    district = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class EmployeeManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Oddiy foydalanuvchi yaratish funksiyasi.
        """
        if not phone_number:
            raise ValueError("The phone number must be provided")
        phone_number = self.normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Superuser yaratish funksiyasi.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)

    def normalize_phone_number(self, phone_number):
        """
        Telefon raqamni normalizatsiya qilish uchun (masalan, +998 formatida).
        """
        return phone_number.strip().replace(" ", "")


class Employee(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(default="images/default-user.png", upload_to="employee-images", blank=True, null=True)

    passport = models.CharField(max_length=15, null=True, blank=True, default=None)

    region = models.CharField(max_length=128)
    district = models.CharField(max_length=128)

    role = models.CharField(choices=(("director", "DIRECTOR"), ("manager", "MANAGER"), ("employee", "EMPLOYEE")), max_length=128, blank=True, null=True)
    position = models.CharField(max_length=128, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = EmployeeManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def full_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.phone_number

    def __str__(self):
        return self.full_name()


class Company(models.Model):
    name = models.CharField(max_length=255)
    stir = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=13, null=True, blank=True, default=None)
    status = models.CharField(max_length=16)

    region = models.CharField(max_length=128)
    district = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name


class Request(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="requests")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    priority = models.IntegerField()
    description = models.TextField()
    long = models.CharField(max_length=256)
    lat = models.CharField(max_length=256)
    file = models.FileField(blank=True)
    status = models.CharField(
        choices=(
            ("pending", "PENDING"),
            ("accepted", "ACCEPTED"),
            ("rejected", "REJECTED"),
            ("on_going", "ON_GOING"),
        ),
        max_length=150,
        default="pending",
    )

    def __str__(self):
        return self.employee.full_name()


class RequestImage(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="request-images/")


class OTP(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="otp")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"OTP for {self.company.phone_number}"


class CompanyToken(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="auth_token")
    key = models.CharField(max_length=40, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        uuid_str = str(uuid.uuid4())
        return hashlib.sha256(uuid_str.encode()).hexdigest()

    def __str__(self):
        return f"Token for {self.company.name}"
