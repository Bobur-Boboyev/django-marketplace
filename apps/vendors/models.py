from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Vendor(models.Model):

    class VendorType(models.TextChoices):
        INDIVIDUAL = "individual", "Individual"
        COMPANY = "company", "Company"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACTIVE = "active", "Active"
        BLOCKED = "blocked", "Blocked"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="vendors"
    )

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    description = models.TextField(blank=True)

    logo = models.ImageField(
        upload_to="vendors/logos/",
        blank=True,
        null=True
    )

    banner = models.ImageField(
        upload_to="vendors/banners/",
        blank=True,
        null=True
    )

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    website = models.URLField(blank=True)

    vendor_type = models.CharField(
        max_length=20,
        choices=VendorType.choices,
        default=VendorType.COMPANY
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()

    postal_code = models.CharField(
        max_length=20,
        blank=True
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    tax_number = models.CharField(
        max_length=100,
        blank=True
    )

    registration_number = models.CharField(
        max_length=100,
        blank=True
    )

    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )

    review_count = models.PositiveIntegerField(default=0)

    last_active_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name