from django.contrib import admin
from .models import *
from ckeditor.widgets import CKEditorWidget
from django import forms
# spaceless убрать пробелы в шаблоне
# {{value|cut " "}} удалить пробелы или любые симполы


class ProductAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Product
        fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name' ,'category', 'created_at' , 'is_publish','price')
    list_display_links=('id','name')
    search_fields= ('name','content')
    list_editable=('is_publish',)
    list_filter=('is_publish','category')
    prepopulated_fields = {'slug':("name",)}
    form = ProductAdminForm


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title' )
    list_display_links=('id','title')
    search_fields= ('title',)
    prepopulated_fields = {'slug':("title",)}


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name' ,'last_name', 'created_at' )
    list_display_links=('id','first_name')


admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Reviews)