from rest_framework.routers import DefaultRouter

from .views import CompanyAuthenticationViewSet, CompanyViewSet, EmployeeViewSet, NewsViewSet, RequestsViewSet

router = DefaultRouter()

router.register("news", NewsViewSet)
router.register("employees", EmployeeViewSet)
router.register("companies", CompanyViewSet)
router.register("requests", RequestsViewSet)
router.register("company-auth", CompanyAuthenticationViewSet, basename="company-auth")
