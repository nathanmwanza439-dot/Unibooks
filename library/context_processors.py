def unread_notifications(request):
    """Context processor that injects unread notifications count for the current user.

    Returns:
        dict: { 'unread_notifications_count': int, 'has_unread_notifications': bool }
    """
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        try:
            count = user.notifications.filter(read=False).count()
        except Exception:
            # In case the User model or notifications relation is not ready yet
            count = 0
    else:
        count = 0

    return {
        'unread_notifications_count': count,
        'has_unread_notifications': bool(count),
    }
