from .models import Product, OrderDetail
import stripe
from django.conf import settings
from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import ProductSerializer


class ProductAPIView(APIView):
    def get(self, request, id=None):
        if id is not None:
            product = Product.objects.get(pk=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            product = Product.objects.all()
            serializer = ProductSerializer(product, many=True)
            return Response(serializer.data)

    def post(self, request, id=None):
        product = get_object_or_404(Product, pk=id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
                          success_url=YOUR_DOMAIN,
                          cancel_url=YOUR_DOMAIN,
                          line_items=[
                              {
                                'price_data': {
                                    'currency': 'inr',
                                    'product_data': {
                                            'name': product.name,
                                                    },
                                    'unit_amount': int(product.price * 100),
                                              },
                                'quantity': 1,
                              }
                            ],
                          mode='payment',
                        )


        print("------------------------")
        print(session.url)
        print("------------------------")
        return Response(session)


class ProductView(ListView):
    model = Product
    template_name = "stripepayment/product_list.html"
    context_object_name = 'product'


class OrderDetailView(DetailView):
    model = Product
    template_name = 'stripepayment/checkout.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://localhost:8000'
@csrf_exempt
def create_checkout_session(request):
    product = get_object_or_404(Product, pk=9)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
                          success_url=YOUR_DOMAIN,
                          cancel_url=YOUR_DOMAIN,
                          line_items=[
                              {
                                'price_data': {
                                    'currency': 'inr',
                                    'product_data': {
                                            'name': product.name,
                                                    },
                                    'unit_amount': int(product.price * 100),
                                              },
                                'quantity': 1,
                              }
                            ],
                          mode='payment',
                        )
    return JsonResponse(session)
