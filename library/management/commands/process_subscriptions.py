from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from library.models import User, Notification, ActionLog
from django.contrib.sessions.models import Session


class Command(BaseCommand):
    help = "Process managed subscriptions: send reminder at 26 days, expire at 31 days"

    def handle(self, *args, **options):
        now = timezone.now()
        users = User.objects.exclude(date_paiement__isnull=True)
        if not users.exists():
            self.stdout.write('No subscriptions with payment date found.')
            return

        for u in users:
            if not u.date_paiement:
                continue
            days = (now - u.date_paiement).days

            # Expire after 31 days
            if days >= 31:
                # Expire access at 31 days: mark account inactive and persist
                if u.is_active:
                    u.is_active = False
                    u.save()
                    # Invalidate any active sessions for the user so they are logged out
                    try:
                        sessions = Session.objects.all()
                        for s in sessions:
                            data = s.get_decoded()
                            if str(data.get('_auth_user_id')) == str(u.pk):
                                s.delete()
                    except Exception:
                        # don't let session cleanup break the command
                        pass

                Notification.objects.create(
                    recipient=u,
                    message="Votre abonnement de 31 jours est arrivé à expiration. Votre accès a été suspendu. Veuillez renouveler au guichet.",
                    type='subscription_expired'
                )
                ActionLog.objects.create(actor=None, action=f"Auto-expired subscription for {u.username}", extra={'days': days})
                self.stdout.write(self.style.WARNING(f"Expired: {u.username} (days={days})"))
                continue

            # Send reminder at 26 days (only once within a 10-day window)
            if 26 <= days < 31:
                window_start = now - timedelta(days=10)
                already = u.notifications.filter(type='subscription_reminder', created_at__gte=window_start).exists()
                if not already:
                    days_left = 31 - days
                    Notification.objects.create(
                        recipient=u,
                        message=f"Rappel : votre abonnement expire dans {days_left} jour(s). Pensez à le renouveler au guichet.",
                        type='subscription_reminder'
                    )
                    ActionLog.objects.create(actor=None, action=f"Sent subscription reminder to {u.username}", extra={'days_left': days_left})
                    self.stdout.write(self.style.SUCCESS(f"Reminder sent: {u.username} (days={days}, days_left={days_left})"))
                else:
                    self.stdout.write(f"Reminder already sent recently: {u.username}")
                continue

            # Otherwise no action
            self.stdout.write(f"No action for {u.username} (days={days})")
