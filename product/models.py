from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS_CHOICES = (
    ('open', 'открытый'),
    ('closed', 'закрытый'),
    ('draft', 'чернровик')
)


class Category(models.Model):
    title = models.CharField('Title', max_length=50)
    slug = models.SlugField('Slug', max_length=50)

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категория'


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='aliexpress_post', verbose_name='Категория')
    title = models.CharField('Название', max_length=50)
    slug = models.SlugField('Слаг', max_length=250, unique_for_date='publish')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aliexpress_posts', verbose_name='Автор')
    body = models.TextField('Содержение')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES)
    image = models.ImageField('Картинка')

    class Meta:
        ordering = ('-publish', )
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def avr_rating(self):
        summ = 0
        ratings = Rating.objects.filter(post=self)
        for rating in ratings:
            summ += rating.rate
        if len(ratings) > 0:
            return summ / len(ratings)
        else:
            return 'Нет рейтинга'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',
                             verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments',
                             verbose_name='Автор')
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.post} --> {self.user}'


class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                            verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        unique_together = (('user', 'post'), )
        index_together = (('user', 'post'), )


class Like(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='likes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='likes')
    is_liked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Favourite(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='favourites')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favourites')
    is_favourite = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'


