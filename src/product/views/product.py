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
    paginate_by = 2

    def post(self, request, *args, **kwargs):
        # NOTE: Unable to remove pagination params for POST request (filtering)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # TODO: Unclear about how size/color/type should be filtered
        # NOTE: Unclear about how date should be filtered

        context = []
        p_data = self.request.POST
        p_title = p_data.get('title')
        p_variant = p_data.get('variant')
        p_pricefrom = p_data.get('price_from')
        p_priceto = p_data.get('price_to')
        p_date = p_data.get('date')
        products = Product.objects.all()

        if p_title:
            products = products.filter(title__icontains=p_title)
        if p_date:
            products = products.filter(created_at__range=[p_date, p_date])

        for p in products:
            variants = []
            for pvp in p.productvariantprice_set.all():
                specs = '/'.join([
                    pvp.product_variant_one.variant_title if pvp.product_variant_one else "",
                    pvp.product_variant_two.variant_title if pvp.product_variant_two else "",
                    pvp.product_variant_three.variant_title if pvp.product_variant_three else "",
                ])
                if p_pricefrom and float(pvp.price) < float(p_pricefrom):
                    continue
                if p_priceto and float(pvp.price) > float(p_priceto):
                    continue
                variants.append({'specs': specs, 'price': pvp.price, 'stock': pvp.stock})
            context.append({'data': p, 'variants': variants})
        return context

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['variants'] = Variant.objects.all()
        return data
