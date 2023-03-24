from django.views import generic

from product.models import Variant, Product, ProductVariant


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
                variant_1 = pvp.product_variant_one.variant_title if pvp.product_variant_one else ""
                variant_2 = pvp.product_variant_two.variant_title if pvp.product_variant_two else ""
                variant_3 = pvp.product_variant_three.variant_title if pvp.product_variant_three else ""
                specs = '/'.join([i for i in (variant_1, variant_2, variant_3) if i != ""])
                if p_pricefrom and float(pvp.price) < float(p_pricefrom): continue
                if p_priceto and float(pvp.price) > float(p_priceto): continue
                if p_variant:
                    if p_variant != variant_1 and p_variant != variant_2 and p_variant != variant_3:
                        continue
                variants.append({'specs': specs, 'price': pvp.price, 'stock': pvp.stock})
            if variants: context.append({'data': p, 'variants': variants})
        return context

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        v_dict = dict()
        variant_values = ProductVariant.objects.values('variant_title').distinct()
        for vtype in Variant.objects.all():
            v_dict[vtype.title] = variant_values.filter(variant=vtype)
        data['variants_values'] = v_dict
        return data
