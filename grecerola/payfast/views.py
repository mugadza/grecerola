from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from .forms import NotifyForm
from .models import PayFastOrder
from .signals import notify


@csrf_exempt
def notify_handler(request):
    """
    Notify URL handler.

    On successful access 'signals.notify' signal is sent.
    Orders should be processed in signal handler.
    """
    id = request.POST.get('m_payment_id', None)
    order = get_object_or_404(PayFastOrder, pk=id)

    form = NotifyForm(request, request.POST, instance=order)
    if not form.is_valid():
        errors = form.plain_errors()[:255]
        order.request_ip = form.ip
        order.debug_info = errors
        order.trusted = False
        order.save()
        raise Http404

    order = form.save()
    notify.send(sender=notify_handler, order=order)
    return HttpResponse()
