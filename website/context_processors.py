from .static_data import COMPANY, get_active_services, get_active_products


def global_context(request):
    """
    Supplies site-wide company info, active services, and active products
    to all templates — no database required.
    """
    return {
        'company': COMPANY,
        'global_services': get_active_services(),
        'global_products': get_active_products(),
    }
