# UniBooks

Une application Django pour la gestion d'une bibliothèque universitaire.

Caractéristiques principales
- Interface Étudiant (connexion par matricule/email)
- Interface Admin/Bibliothèque (gestion des comptes, livres, demandes)
- Emprunts soumis à validation admin
- Réservations, likes, commentaires
- Notifications et logs d'actions

Installation (macOS, zsh)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Notes
- Aucun enregistrement public; les comptes étudiants sont créés par l'admin.
- Mot de passe par défaut: `12345678` (forcé au premier login à être changé).

Scheduler (tâches planifiées)
-----------------------------

UniBooks inclut deux commandes de gestion à exécuter régulièrement :

- `send_due_reminders` : envoie des rappels pour les emprunts proches de leur date d'échéance et les emprunts en retard.
- `process_subscriptions` : envoie des rappels d'abonnement (J+26) et expire automatiquement les abonnements (J+31).

Exemple de crontab (exécuter `crontab -e` pour l'utilisateur qui gère l'application). Adaptez les chemins vers votre répertoire et votre interpréteur Python virtuel.

```cron
# Exécuter send_due_reminders tous les jours à 03:00
0 3 * * * cd /path/to/UniBooks && /path/to/venv/bin/python3 manage.py send_due_reminders >> /var/log/unibooks/send_due_reminders.log 2>&1

# Exécuter process_subscriptions tous les jours à 03:10
10 3 * * * cd /path/to/UniBooks && /path/to/venv/bin/python3 manage.py process_subscriptions >> /var/log/unibooks/process_subscriptions.log 2>&1
```

Conseils opérationnels :

- Utilisez des chemins absolus (`/Users/you/...` ou `/srv/...`) dans la crontab. Ne comptez pas sur `PATH` ou sur l'activation implicite du virtualenv.
- Créez le dossier de logs (`/var/log/unibooks`) et donnez les droits à l'utilisateur qui lance cron.
- Testez les commandes manuellement avant de les ajouter au cron :

```bash
/path/to/venv/bin/python3 manage.py send_due_reminders
/path/to/venv/bin/python3 manage.py process_subscriptions
```

Alternatives
------------

- Si vous préférez une solution plus robuste, utilisez un scheduler applicatif (Celery + Celery Beat) ou un gestionnaire de processus (systemd timers) pour une meilleure observabilité et redémarrage automatique.
- Pour les environnements conteneurisés, combinez des cron jobs dans un conteneur dédié ou utilisez des services cloud (Cloud Scheduler, RQ Scheduler, etc.).

Voir `bin/cron_example.sh` pour un petit helper qui affiche et installe un exemple de crontab.
