import random
import string

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from apps.common.models import TimeStampedUUIDModel
from apps.properties.managers import PropertyPublishedManager

User = get_user_model()


class AdvertType(models.TextChoices):
    FOR_SALE = "For Sale", _("For Sale")
    FOR_RENT = "For Rent", _("For Rent")
    AUCTION = "Auction", _("Auction")


class PropertyType(models.TextChoices):
    HOUSE = "House", _("House")
    APARTMENT = "Apartment", _("Apartment")
    OFFICE = "Office", _("Office")
    WAREHOUSE = "Warehouse", _("Warehouse")
    COMMERCIAL = "Commercial", _("Commercial")
    OTHER = "Other", _("Other")


class Property(TimeStampedUUIDModel):
    user = models.ForeignKey(
        User,
        verbose_name=_("Agent,Seller or Buyer"),
        related_name="agent_buyer",
        on_delete=models.DO_NOTHING,
    )
    title = models.CharField(verbose_name=_("Property Title"), max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    ref_code = models.CharField(
        verbose_name=_("Property Reference Code"),
        max_length=255,
        unique=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        default="Default description...update me please....",
    )
    country = CountryField(
        verbose_name=_("Country"),
        default="KE",
        blank_label="(select country)",
    )
    city = models.CharField(verbose_name=_("City"), max_length=180, default="Nairobi")
    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=100, default="140"
    )
    street_address = models.CharField(
        verbose_name=_("Street Address"), max_length=150, default="KG8 Avenue"
    )
    property_number = models.IntegerField(
        verbose_name=_("Property Number"),
        validators=[MinValueValidator(1)],
        default=112,
    )
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=8, decimal_places=2, default=0.0
    )
    tax = models.DecimalField(
        verbose_name=_("Property Tax"),
        max_digits=6,
        decimal_places=2,
        default=0.15,
        help_text="15% property tax charged",
    )
    plot_area = models.DecimalField(
        verbose_name=_("Plot Area(m^2)"), max_digits=8, decimal_places=2, default=0.0
    )
    total_floors = models.IntegerField(verbose_name=_("Number of floors"), default=0)
    bedrooms = models.PositiveSmallIntegerField(verbose_name=_("Bedrooms"), default=1)
    bathrooms = models.PositiveSmallIntegerField(verbose_name=_("Bathrooms"), default=1)
    advert_type = models.CharField(
        verbose_name=_("Advert Type"),
        max_length=50,
        choices=AdvertType.choices,
        default=AdvertType.FOR_SALE,
    )

    property_type = models.CharField(
        verbose_name=_("Property Type"),
        max_length=50,
        choices=PropertyType.choices,
        default=PropertyType.OTHER,
    )

    cover_photo = models.ImageField(
        verbose_name=_("Main Photo"),
        default="simple_images/house_sample.jpg",
        upload_to="mediafiles/property/",
        null=True,
        blank=True,
    )
    published_status = models.BooleanField(
        verbose_name=_("Published Status"), default=False
    )
    views = models.IntegerField(verbose_name=_("Total Views"), default=0)

    objects = models.Manager()
    published = PropertyPublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        if not self.ref_code:
            self.ref_code = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=10)
            )
        super().save(*args, **kwargs)

    @property
    def final_property_price(self):
        tax_percentage = self.tax
        property_price = self.price
        tax_amount = round(tax_percentage * property_price, 2)
        price_after_tax = float(round(property_price + tax_amount, 2))
        return price_after_tax


class PropertyImages(TimeStampedUUIDModel):
    property = models.ForeignKey(
        Property, related_name="property_images", on_delete=models.CASCADE
    )

    photo = models.ImageField(
        default="simple_images/interior_sample.jpg",
        upload_to="mediafiles/property/",
        validators=[FileExtensionValidator(allowed_extensions=("jpg", "jpeg", "png"))],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.property.id} - {self.photo}"

    class Meta:
        verbose_name = _("Image Property")
        verbose_name_plural = _("Image Properties")


class PropertyViews(TimeStampedUUIDModel):
    ip = models.CharField(verbose_name=_("IP Address"), max_length=250)
    property = models.ForeignKey(
        Property, related_name="property_views", on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"Total views on - {self.property.title} is - {self.property.views} view(s)"
        )

    class Meta:
        verbose_name = _("Total Views on Property")
        verbose_name_plural = _("Total Property Views")
