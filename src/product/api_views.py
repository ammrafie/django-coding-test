from rest_framework.generics import CreateAPIView
from .serializers import ProductSerializer


class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer


# class ProductVariantCreate(CreateAPIView):
#     serializer_class = ProductVariantSerializer
#     def perform_create(self, serializer):
#         product_data = self.request.data.get('product', {})
#         variants_data = self.request.data.get('variants', [])
#         product_serializer = ProductSerializer(data=product_data)
#         if not product_serializer.is_valid():
#             return Response(
#                 {'error': 'Invalid product data!!!'}, status=status.HTTP_400_BAD_REQUEST
#             )
#         product = product_serializer.save()
#         for variant in variants_data:
#             variant['product'] = product.id
#             variant_serializer = ProductVariantSerializer(data=variant)
#             if variant_serializer.is_valid(): variant_serializer.save()
#             variant_serializer.save()
#         return Response({'success': 'Variants saved successfully.'}, status=status.HTTP_201_CREATED)
