from django.urls import path
from django.views.generic import TemplateView

from .views import GiftListView, cancel, detail

urlpatterns = [
    path('', GiftListView.as_view(), name='gift_list'),
    path('<int:id>/', detail, name='gift_detail'),
    path('<int:giver_id>/cancel/<key>/', cancel, name='gift_cancel'),
    path('thanks-given/', TemplateView.as_view(
        template_name='gift_registry/thanks_given.html'),
        name='thanks_given'),
    path('thanks-cancel/', TemplateView.as_view(
        template_name='gift_registry/thanks_cancel.html'),
        name='thanks_cancel'),
]
