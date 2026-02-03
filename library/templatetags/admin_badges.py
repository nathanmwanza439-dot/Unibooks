from django import template
from django.urls import reverse
from library.models import MissingRequest
from library.models import BorrowRequest, Reservation

register = template.Library()


@register.simple_tag
def unhandled_missing_count():
    """Return the count of MissingRequest objects not yet handled."""
    return MissingRequest.objects.filter(handled_at__isnull=True).count()


@register.simple_tag
def missingrequest_admin_url():
    """Return the admin changelist URL for MissingRequest."""
    try:
        return reverse('admin:library_missingrequest_changelist')
    except Exception:
        return '#'


@register.simple_tag
def pending_borrow_count():
    """Return the count of BorrowRequest objects that need admin attention (PENDING)."""
    return BorrowRequest.objects.filter(status='PENDING').count()


@register.simple_tag
def borrowrequest_admin_url():
    try:
        return reverse('admin:library_borrowrequest_changelist')
    except Exception:
        return '#'


@register.simple_tag
def pending_reservation_count():
    """Return the count of Reservation objects that may need attention (ACTIVE)."""
    return Reservation.objects.filter(status='ACTIVE').count()


@register.simple_tag
def reservation_admin_url():
    try:
        return reverse('admin:library_reservation_changelist')
    except Exception:
        return '#'
