#-*- coding: utf-8 -*-
from django.db.models import Count, Sum, Prefetch
from django.shortcuts import render
# Create your views here.
from django.views.generic import ListView

from mailer.models import Company, Contact


class IndexView(ListView):
    template_name = "mailer/index.html"
    model = Company
    paginate_by = 100

    def get_queryset(self):
        return Company.objects\
            .prefetch_related("orders")\
            .prefetch_related(
                Prefetch(
                    "contacts", queryset=Contact.objects.annotate(get_order_count=Count("orders", distinct=True))
                )
            )\
            .annotate(get_order_count=Count("orders", distinct=True))\
            .annotate(get_order_sum=Sum("orders__total"))
