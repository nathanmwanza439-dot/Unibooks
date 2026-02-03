# Generated automated migration for subscription refactor
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_add_subscription_managed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_paiement',
            field=models.DateTimeField(blank=True, null=True, help_text='Date et heure du paiement (format UTC)'),
        ),
        migrations.AddField(
            model_name='user',
            name='date_expiration',
            field=models.DateTimeField(blank=True, null=True, editable=False),
        ),
        migrations.RemoveField(
            model_name='user',
            name='subscription_managed',
        ),
        migrations.RemoveField(
            model_name='user',
            name='subscription_start',
        ),
    ]
