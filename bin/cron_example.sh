#!/usr/bin/env bash
# Small helper that prints an example crontab for UniBooks and explains how to install it.
# Edit the paths before installing.

PROJECT_DIR="/path/to/UniBooks"         # <-- replace
VENV_PYTHON="/path/to/venv/bin/python3" # <-- replace
LOG_DIR="/var/log/unibooks"             # <-- replace if desired

cat <<'CRON'
# --- UniBooks example crontab (edit paths first) ---
# Run reminders at 03:00 daily
0 3 * * * cd /path/to/UniBooks && /path/to/venv/bin/python3 manage.py send_due_reminders >> /var/log/unibooks/send_due_reminders.log 2>&1

# Run subscription processing at 03:10 daily
10 3 * * * cd /path/to/UniBooks && /path/to/venv/bin/python3 manage.py process_subscriptions >> /var/log/unibooks/process_subscriptions.log 2>&1
# ---------------------------------------------------
CRON

echo
echo "To install this crontab (after editing the file), run:" 
echo "  crontab -e"
echo "and paste the edited lines, or run:"
echo "  (crontab -l; echo \"# UniBooks jobs\"; echo \"0 3 * * * cd $PROJECT_DIR && $VENV_PYTHON manage.py send_due_reminders >> $LOG_DIR/send_due_reminders.log 2>&1\"; echo \"10 3 * * * cd $PROJECT_DIR && $VENV_PYTHON manage.py process_subscriptions >> $LOG_DIR/process_subscriptions.log 2>&1\") | crontab -"

echo
echo "Make sure the log directory exists and is writable by the cron user:" 
echo "  sudo mkdir -p $LOG_DIR && sudo chown $(whoami) $LOG_DIR"
