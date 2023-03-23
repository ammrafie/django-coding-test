from django.views import generic

from product.models import Variant, Product


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class ListProductView(generic.ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = "context"

    def get_queryset(self):
        context = []
        for p in Product.objects.all():
            variants = []
            for pvp in p.productvariantprice_set.all():
                specs = '/'.join([
                    pvp.product_variant_one.variant_title if pvp.product_variant_one else "",
                    pvp.product_variant_two.variant_title if pvp.product_variant_two else "",
                    pvp.product_variant_three.variant_title if pvp.product_variant_three else "",
                ])
                variants.append({'specs': specs, 'price': pvp.price, 'stock': pvp.stock})
            context.append({'data': p, 'variants': variants})
        return context
