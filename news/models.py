from django.db import models
from django.urls import reverse
from django.conf import settings


class Product(models.Model):
    category = models.ForeignKey('Category',on_delete=models.PROTECT)
    name = models.CharField(max_length=150,verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='URL продукта', unique=True)
    content = models.TextField(verbose_name='Контент')
    price = models.DecimalField( decimal_places=2, max_digits=9)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='СОздано')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/',verbose_name='Изображение')
    is_publish = models.BooleanField(default=True)
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('view_prdouct',kwargs={"slug":self.slug})

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='Продукт'
        verbose_name_plural='Продукты'
        ordering=['-created_at',]


class Category(models.Model):
    title = models.CharField(max_length=150,db_index=True,verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='URL категории', unique=True)

    def get_absolute_url(self):
        return reverse('category',kwargs={"slug":self.slug})

    def __str__(self):
        return self.title

        
    class Meta:
        verbose_name='Категория'
        verbose_name_plural='Категории'
        ordering=['title']


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='customer',on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format( self.user)


class Order(models.Model):

    STATUS_NEW ='new'
    STATUS_IN_PROGRESS='in_progress'
    STATUS_READY= 'is_ready'
    STATUS_COMPLETED= 'completed'
    STATUS_DEACTIVE='deactive'

    STATUS_CHOICES= (
    (STATUS_NEW,'Новый заказ'),
    (STATUS_IN_PROGRESS,'Заказ в обработке'),
    (STATUS_READY,'Заказ готов'),
    (STATUS_COMPLETED,'Заказ выполнен'),
    (STATUS_DEACTIVE,'Заказ Отменен')
)
    customer =  models.ForeignKey(Customer,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email= models.EmailField(max_length=60, verbose_name='Емайл')
    adress = models.CharField(max_length=60, verbose_name='Город', null=True, blank=True)
    final_price = models.PositiveIntegerField(verbose_name='Сумма заказа')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='СОздано')
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказа',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )

    def __str__(self):
        return self.customer.user.username

    class Meta:
        verbose_name='Заказ'
        verbose_name_plural='Заказы'
        ordering=['-created_at',]


class Reviews(models.Model):

    name= models.CharField(max_length=255, verbose_name='Имя')
    text= models.TextField('Сообщение',max_length=500)
    product=models.ForeignKey(Product,verbose_name='Продукт',on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True,db_index=True,verbose_name='Добавлено')

    def __str__(self):
        return f"{self.name}-{self.product}"

    class Meta:
        verbose_name='Отзыв'
        verbose_name_plural='Отзывы'
