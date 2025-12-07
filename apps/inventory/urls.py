from django.urls import path

from .views import CatalogView, ProductDetailView

urlpatterns = [
    path("", CatalogView.as_view(), name="catalog"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
]
