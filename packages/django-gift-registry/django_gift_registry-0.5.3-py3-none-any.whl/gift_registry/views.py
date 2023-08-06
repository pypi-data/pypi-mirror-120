from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from gift_registry.forms import GiverForm
from gift_registry.models import Gift, Giver


class GiftListView(ListView):
    """Show all live gifts."""

    queryset = Gift.objects.filter(live=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_name'] = settings.GIFT_REGISTRY_SETTINGS['EVENT_NAME']
        return context


def detail(request, id):
    """Show details of a particular gift."""
    gift = get_object_or_404(Gift, pk=id)
    giver = Giver(gift_id=id)
    if request.method == 'POST':
        giver_form = GiverForm(request.POST, instance=giver)
        if giver_form.is_valid():
            giver_form.save()
            return redirect('thanks_given')
        else:
            return render(request, 'gift_registry/gift_detail.html', {
                'object': gift,
                'giver_form': giver_form,
            })
    else:
        return render(request, 'gift_registry/gift_detail.html', {
            'object': gift,
            'giver_form': GiverForm(instance=giver),
        })


def cancel(request, giver_id, key):
    giver = get_object_or_404(Giver, id=giver_id)
    if giver.secret_key() != key:
        raise PermissionDenied

    giver.delete()
    return redirect('thanks_cancel')
