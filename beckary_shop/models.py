from django.db import models
from django.urls import reverse
from django.core import serializers



class Section(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    url = models.URLField()
    img = models.ImageField(upload_to='section/')
    def get_absolute_url(self):
        return reverse('beckary_shop:cat_list', args=[self.slug])

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    section = models.ForeignKey(Section, related_name='category', on_delete=models.CASCADE)
    url = models.URLField()
    img = models.ImageField()
    def get_absolute_url(self):
        return reverse('beckary_shop:prod_list', args=[self.section.slug, self.slug])

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField()
    img = models.ImageField()
    def get_absolute_url(self):
        return reverse('beckary_shop:prod_detail', args=[self.category.section.slug, self.category.slug, self.slug])

    def __str__(self):
        return self.slug

def live_search(q):
    objects = Product.objects.filter(name__icontaines = q,)
                           #slug__icontaines = q,
                           #description__icontaines = q)
    json = []
    for item in objects:
        json.append(serializers.serialize('json', item))

    return json