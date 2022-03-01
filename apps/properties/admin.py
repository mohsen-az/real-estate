from django.contrib import admin

from apps.properties.models import Property, PropertyImages, PropertyViews


class PropertyImagesInline(admin.TabularInline):
    model = PropertyImages
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ["title", "country", "advert_type", "property_type"]
    list_filter = ["advert_type", "property_type", "country"]
    inlines = [PropertyImagesInline]


@admin.register(PropertyViews)
class PropertyViewsAdmin(admin.ModelAdmin):
    pass
