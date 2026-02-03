from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import BorrowRequest, Reservation, Notification, ActionLog
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(pre_save, sender=BorrowRequest)
def borrow_pre_save(sender, instance, **kwargs):
    """Detect status transition to APPROVED and mark instance for post_save work."""
    if not instance.pk:
        return
    try:
        old = BorrowRequest.objects.get(pk=instance.pk)
    except BorrowRequest.DoesNotExist:
        return
    if old.status != 'APPROVED' and instance.status == 'APPROVED':
        # carry a flag to post_save (same instance object during save)
        setattr(instance, '_was_approved', True)


@receiver(post_save, sender=BorrowRequest)
def borrow_post_save(sender, instance, created, **kwargs):
    """Create notifications when a borrow request is created or approved.

    - On creation: confirmation notification for the student.
    - On approval: approval notification (with dates) and action log; email sent when possible.
    """
    # Confirmation on creation
    if created:
        msg = f"Votre demande d'emprunt pour \"{instance.book.title}\" a été reçue et est en attente de validation."
        Notification.objects.create(recipient=instance.student, message=msg, type='info')
        ActionLog.objects.create(actor=instance.student, action=f'Created borrow request {instance.pk}')

    # Approval transition
    if getattr(instance, '_was_approved', False) or (created and instance.status == 'APPROVED'):
        due = getattr(instance, 'due_date', None)
        borrow_date = getattr(instance, 'borrow_date', None)
        msg = f"Votre emprunt pour \"{instance.book.title}\" a été accepté."
        if borrow_date:
            msg += f" Emprunté le {borrow_date}."
        if due:
            msg += f" Date d'échéance : {due}."
        Notification.objects.create(recipient=instance.student, message=msg, type='borrow_approved')
        # send email (best-effort)
        try:
            send_mail('Emprunt accepté - UniBooks', msg, settings.DEFAULT_FROM_EMAIL, [instance.student.email], fail_silently=True)
        except Exception:
            pass
        ActionLog.objects.create(actor=None, action=f'Borrow {instance.pk} approved and notification sent')


@receiver(pre_save, sender=Reservation)
def reservation_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Reservation.objects.get(pk=instance.pk)
    except Reservation.DoesNotExist:
        return
    if old.status != instance.status:
        setattr(instance, '_status_changed', True)


@receiver(post_save, sender=Reservation)
def reservation_post_save(sender, instance, created, **kwargs):
    # Notify on reservation status changes
    if created:
        Notification.objects.create(recipient=instance.student,
                                    message=f"Votre réservation pour \"{instance.book.title}\" a été enregistrée.",
                                    type='info')
        ActionLog.objects.create(actor=instance.student, action=f'Created reservation {instance.pk}')
        return

    if getattr(instance, '_status_changed', False):
        if instance.status == 'FULFILLED':
            Notification.objects.create(recipient=instance.student,
                                        message=f"Votre réservation pour \"{instance.book.title}\" est prête à être récupérée.",
                                        type='reservation_ready')
            ActionLog.objects.create(actor=None, action=f'Reservation {instance.pk} fulfilled; notified student')
        elif instance.status == 'CANCELLED':
            Notification.objects.create(recipient=instance.student,
                                        message=f"Votre réservation pour \"{instance.book.title}\" a été annulée.",
                                        type='reservation_cancelled')
            ActionLog.objects.create(actor=None, action=f'Reservation {instance.pk} cancelled; notified student')



@receiver(post_save, sender='library.MissingRequest')
def missingrequest_post_save(sender, instance, created, **kwargs):
    """Notify staff/admin users when a MissingRequest (demande d'achat) is created.

    We create a Notification for each staff user and an ActionLog entry. Also attempt
    to send an email to staff (best-effort via send_mail).
    """
    if not created:
        return
    # Build message
    msg = f"Nouvelle demande d'achat: \"{instance.title}\" par {instance.student}."

    # Notify each staff user
    staff_users = User.objects.filter(is_staff=True)
    for admin in staff_users:
        Notification.objects.create(recipient=admin, message=msg, type='missing_request')

    # Action log
    ActionLog.objects.create(actor=instance.student, action=f'Created MissingRequest {instance.pk}')

    # Try sending a single email to DEFAULT_FROM_EMAIL -> could be improved to list of staff
    try:
        send_mail('Nouvelle demande d\'achat - UniBooks', msg, settings.DEFAULT_FROM_EMAIL, [u.email for u in staff_users if u.email], fail_silently=True)
    except Exception:
        pass
