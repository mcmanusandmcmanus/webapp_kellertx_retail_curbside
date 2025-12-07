from django.db.models import Q
from django.views.generic import DetailView, ListView

from .models import Category, Product


class CatalogView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "inventory/catalog.html"
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related("category")
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        search = self.request.GET.get("q")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search) | Q(sku__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        ctx["active_category"] = self.request.GET.get("category", "")
        ctx["query"] = self.request.GET.get("q", "")
        return ctx


class ProductDetailView(DetailView):
    model = Product
    template_name = "inventory/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
