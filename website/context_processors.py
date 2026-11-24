from .models import CompanySetting, Service, Project

def global_context(request):
    """
    Supplies site-wide company settings, active services, and active products
    so header, navigation, and footer stay in sync across all pages.
    """
    try:
        company = CompanySetting.get_settings()
    except Exception:
        company = None

    try:
        services = Service.objects.filter(is_active=True).order_by('order', 'id')
    except Exception:
        services = []

    try:
        products = Project.objects.filter(is_active=True).order_by('order', 'id')
    except Exception:
        products = []

    return {
        'company': company,
        'global_services': services,
        'global_products': products,
    }
