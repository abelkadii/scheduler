from plyer import notification
from utils import settings

def notify(title, message, app_name='Notifier', app_icon=settings.get('paths').get('icon'), timeout=3):
    notification.notify(
        app_name=app_name,
        title=title,
        message=message,
        app_icon=app_icon,
        timeout=timeout
    )

