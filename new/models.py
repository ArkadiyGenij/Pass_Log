from django.db import models


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    content = models.TextField(verbose_name='сообщение')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='дата обновления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'новости'


class NewsImage(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    image = models.ImageField(upload_to='news/%Y/%m/%d', verbose_name='картинка')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='дата обновления')
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='новость')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'
