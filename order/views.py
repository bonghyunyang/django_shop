from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from user.decorators import login_required
from django.db import transaction
from .forms import RegisterForm
from .models import Order
from user.models import User
from product.models import Product


@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        with transaction.atomic():
            prod = Product.objects.get(pk=form.data.get('product'))
            order = Order(
                quantity=form.data.get('quantity'),
                product=prod,
                order_user=User.objects.get(email=self.request.session.get('order_user'))
            )
        order.save()
        prod.stock -= int(form.data.get('quantity'))
        prod.save()

        return super().form_valid(form)


def form_invalid(self, form):
    return redirect('/product/' + str(form.data.get('product')))


def get_form_kwargs(self, **kwargs):
    kw = super().get_form_kwargs(**kwargs)
    kw.update({
        'request': self.request
    })
    return kw


@method_decorator(login_required, name='dispatch')
# 클래스 안에 디스패치 함수가 있으며, 이를 감싸주는 데코레이터를 구현
class OrderList(ListView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order_list'

    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(order_user__email=self.request.session.get('user'))
        return queryset
