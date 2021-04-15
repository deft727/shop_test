from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect
from django.views.generic import ListView,DetailView,View
from .models import *
from .forms import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string,get_template
from django.contrib.auth import authenticate,login
from django.urls import reverse_lazy
from .utils import MyMixin
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,logout
from django.core.mail import send_mail
from django.db.models import F
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.conf import settings


@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cartdetail=cart.cart
    for key, value in cartdetail.items():
        if key == str(product.id):
            if(value['quantity'] < 1):
                messages.add_message(request,messages.ERROR,'Ошибка регистрации')
                return redirect('cart_detail')
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_detail(request):
    return render(request, 'products/cart_detail.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail=send_mail(form.cleaned_data['subject'], form.cleaned_data['content'],form.cleaned_data['email'],['zarj09@gmail.com'], fail_silently=False)
            if mail:
                messages.success(request,'Письмо отправлено')
                return redirect ('contact')
            else:
                messages.error(request,'Ошибка отправки')
                return redirect ('contact')
    else:
         form = ContactForm()
    return render(request,'products/contact.html',{"form":form,'title':'связь'})


class IndexView(ListView):
    model = Product
    template_name= 'products/index.html'
    context_object_name = 'products'
    paginate_by = 2
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'главная страница'
        return context

    def get_queryset(self):
        return Product.objects.filter(is_publish=True)


class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            messages.add_message(request,messages.ERROR,'Вы уже залогинены')
            return redirect('home')
        form=RegistrationForm(request.POST or None)
        title = 'Регистрация'
        context = {
            'title':title,
            'form':form,
        }
        return render(request,'products/register.html',context)
    
    def post(self,request,*args,**kwargs):
        form= RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.username=form.cleaned_data['username']
            new_user.email=form.cleaned_data['email']
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user= authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            login(request,user)
            messages.add_message(request,messages.SUCCESS,'registration completed successfully')
            return redirect('home')
        else:
            messages.add_message(request,messages.ERROR,'Ошибка регистрации')
        context={'form':form,}
        return render(request,'products/register.html',context)


class LoginView(View):
    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            messages.add_message(request,messages.ERROR,'Вы уже залогинены')
            return redirect('home')
        form = LoginForm(request.POST or None)
        title = 'Логин'
        context= {'title':title,
        'form':form,
        }
        return render(request,'products/login.html',context)

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST or None)
        if form.is_valid():
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            if '@' in username:
                user1= User.objects.filter(email=username).first()
                user= authenticate(username=user1,password=password)
            else:
                user= authenticate(username=username,password=password)
            if user:
                login(request,user)
            return HttpResponseRedirect('/')
        context={'form':form,}
        return render(request,'products/login.html',context)


class AddReview(View):
    
    def post(self,request,id):
        product = Product.objects.get(id=id)
        form=ReviewsForm(request.POST or None)
        if  form.is_valid():
            form=form.save(commit=False)
            form.name = request.user
            form.product=product
            form.save()
            messages.add_message(request,messages.SUCCESS,'Комментарий добавлен')
        else:
            messages.add_message(request,messages.ERROR,'Ошибка')
        return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))


class ProductByCategory(ListView):
    model = Product
    template_name= 'products/index.html'
    context_object_name = 'products'
    allow_empty = False 
    paginate_by = 2

    def get_queryset(self):
            return Product.objects.filter(category__slug=self.kwargs['slug'],is_publish=True)

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class ProductView(DetailView):
    model= Product
    template_name= 'products/view_products.html'
    context_object_name = 'product'
    
    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        context['title']= self.get_object().name
        context['form']= ReviewsForm()
        return context


class MakeOrderView(MyMixin,View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        cart = Cart(request)
        cart=cart.cart

        if bool(cart) is False or not request.user.is_authenticated:
            return redirect('home')

        title='checkout'
        context = {
            'title':title,
            'form': form
        }
        return render(request, 'products/checkout.html', context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        cart = Cart(request)
        cartdetail=cart.cart
        customer = Customer.objects.get_or_create(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = request.user.customer
            new_order.final_price=self.get_final_price()
            new_order.save()
            cart.clear()
            subject = "Заказ на сайте 12312312"
            to = [new_order.email,settings.ADMIN]
            from_email = 'test@example.com'
            ctx = {
                'order': new_order,
            }
            message = get_template('message/message.html').render(ctx)
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()
            messages.add_message(request,messages.SUCCESS,'спасибо за заказ, проверьте емайл')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class ProfileView(View):
    def get (self,request,*args,**kwargs):
        if not  request.user.is_authenticated:
            messages.add_message(request,messages.ERROR,'Нужна регистрация')
            return redirect('register')
        customer = request.user
        title = 'Профиль: '+ request.user.username
        return render(request,'products/profile.html',{'title':title,
        'customer':customer,
 })