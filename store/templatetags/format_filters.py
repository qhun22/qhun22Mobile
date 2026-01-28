from django import template

register = template.Library()

@register.filter
def format_number(value):
    """
    Format number with thousand separator using Vietnamese locale (1.000.000 format)
    
    Usage in template: {{ number|format_number }}
    Example: 1000000|format_number => 1.000.000
    """
    try:
        # Convert to float first, then to int if it's a whole number
        num = float(value)
        if num == int(num):
            num = int(num)
        
        # Format with Vietnamese locale (dot as thousand separator)
        return f"{num:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return value
