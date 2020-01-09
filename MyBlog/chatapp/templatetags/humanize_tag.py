from django import template

register = template.Library()

MOMENT = 120  # duration in seconds within which the time difference


# will be rendered as 'a moment ago'

@register.filter
def naturalTimeDifference(value):
    """
    Finds the difference between the datetime value given and now()
    and returns appropriate humanize form
    """

    from datetime import datetime

    if isinstance(value, datetime):
        delta = datetime.now() - value.replace(tzinfo=None)
        if delta.days > 1:
            return value.strftime("%d-%b-%Y %I:%M %p")  # Wednesday
        elif delta.days == 1:
            return 'yesterday'  # yesterday
        elif delta.seconds > 3600:
            return str(int(delta.seconds / 3600)) + ' hours ago'  # 3 hours ago
        elif delta.seconds > MOMENT:
            return str(int(delta.seconds / 60)) + ' minutes ago'  # 29 minutes ago
        else:
            return 'just now'  # a moment ago
    else:
        return str(value)