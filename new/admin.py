from django.contrib import admin
from django.utils.safestring import mark_safe

from new.models import NewsImage, News


# Register your models here.
class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 2
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="250" style="max-height: auto; object-fit: contain;"/>')
        return "—"

    preview.short_description = 'Превью'
    preview.allow_tags = True


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'create_at')
    search_fields = ('title', 'content')
    readonly_fields = ('get_preview', 'create_at', 'update_at')
    inlines = [NewsImageInline]

    def get_preview(self, obj):
        if obj.preview:
            return mark_safe(
                f'<img src="{obj.preview.url}" width="400" style="max-height: auto; object-fit: contain;"/>')
        return "—"

    get_preview.short_description = 'Текущая заставка'
    get_preview.allow_tags = True
