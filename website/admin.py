from django.contrib import admin

from .models import (
Service,
Project,
Blog,
Testimonial,
Contact,
Newsletter
)



admin.site.register(Service)

admin.site.register(Project)

admin.site.register(Blog)

admin.site.register(Testimonial)

admin.site.register(Contact)

admin.site.register(Newsletter)
