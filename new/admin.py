from django.contrib import admin
from django.utils.safestring import mark_safe

from new.models import NewsImage, News


# Register your models here.
class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 3


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at', 'get_preview', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'create_at')
    search_fields = ('title', 'content')
    readonly_fields = ('get_preview', 'create_at', 'update_at')

    def get_preview(self, obj):
        if obj.preview:
            return mark_safe(
                f'<img src="{obj.preview.url}" width="200" style="max-height: 120px; object-fit: contain;"/>')
        return "—"

    get_preview.short_description = 'Текущая заставка'
    get_preview.allow_tags = True
