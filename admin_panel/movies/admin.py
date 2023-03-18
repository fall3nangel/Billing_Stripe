from django.contrib import admin

from movies.models import Filmwork, Product, FilmworkProduct


class FilmworkProductInline(admin.TabularInline):
    model = FilmworkProduct
    extra = 3


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
    )
    list_filter = ("type",)
    search_fields = ("title", "description", "id")
    inlines = (FilmworkProductInline,)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
    )
    search_fields = ("name",)
