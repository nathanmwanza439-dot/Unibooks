# Déploiement sur Railway (avec PostgreSQL)

Ce guide explique pas à pas comment déployer UniBooks sur Railway et activer PostgreSQL.

Prérequis
- Un compte Railway (https://railway.app)
- Un dépôt Git (GitHub/GitLab) contenant ce projet
- Variables d'environnement secrètes (SECRET_KEY, etc.)

Étapes

1) Pousser le code

   Poussez votre dépôt sur GitHub si ce n'est pas déjà fait.

2) Créer un nouveau projet Railway et le connecter au repo

   - Créez un projet et connectez votre dépôt.

3) Ajouter PostgreSQL

   - Dans Railway, ajoutez un plugin "Postgres" (New plugin → Postgres).
   - Railway créera une base et injectera automatiquement `DATABASE_URL` dans les variables d'environnement du service.

4) Configurer les variables d'environnement

   Dans les Settings / Variables d'environnement de votre service Railway, ajoutez au moins :

   - `DJANGO_SECRET_KEY` = une valeur secrète forte
   - `DJANGO_DEBUG` = 0
   - `DJANGO_ALLOWED_HOSTS` = `your-app.up.railway.app` (ou votre domaine personnalisé)

   `DATABASE_URL` est fournie automatiquement par Railway lorsque vous ajoutez Postgres.

   Optionnel (S3 pour MEDIA, email, etc.) :
   - `AWS_STORAGE_BUCKET_NAME`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_REGION_NAME`, etc.
   - `DJANGO_EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, etc.

5) Build & Start

   - Le repo contient un `Procfile` et `start.sh` : Railway utilisera ces fichiers.
   - `start.sh` exécute `migrate`, `collectstatic`, puis démarre Gunicorn. Il définit par défaut `DJANGO_SETTINGS_MODULE=unibooks.settings_production` si non fourni.

6) Migrer et vérifier

   - Après le premier déploiement, Railway lancera le process qui appliquera automatiquement les migrations.
   - Vérifiez les logs pour vous assurer que `migrate` s'est bien exécuté et que `collectstatic` n'a pas d'erreur.

Conseils et dépannage

- Si `collectstatic` échoue à cause d'un manifest manquant, vérifiez `STATICFILES_STORAGE` et les fichiers statiques. Le fichier `unibooks/settings_production.py` force `CompressedManifestStaticFilesStorage`.
- Si vous préférez stocker les fichiers médias sur S3, définissez les variables AWS et `AWS_STORAGE_BUCKET_NAME`; `unibooks/settings.py` bascule automatiquement sur `S3Boto3Storage` si cette variable est définie.
- Pour tester localement, copiez `.env.example` en `.env` (ou exportez les variables) puis :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_SECRET_KEY='dev-key'
export DJANGO_DEBUG=1
python3 manage.py migrate
python3 manage.py runserver
```

Sécurité

- Ne commitez jamais `DJANGO_SECRET_KEY` ni d'autres secrets dans le repo.
- Utilisez les variables d'environnement fournies par Railway ou un gestionnaire de secrets.

Suivant

- Je peux ajouter une GitHub Action qui exécute `manage.py check` et les tests à chaque push.
- Je peux aussi ajouter un script de backup ou une recommandation pour la sauvegarde PostgreSQL.
