from django.contrib import admin
from django.utils.html import format_html

from new.models import NewsImage, News


# Register your models here.
class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 3
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = "Превью"


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at')
    inlines = [NewsImageInline]
