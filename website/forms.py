from django import forms
from .models import Contact, Service, Project


class ContactForm(forms.ModelForm):
    topic = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Area of Interest / Topic",
        help_text="Select a specific product, IT service, or general enquiry"
    )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'topic', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'you@company.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 98765 43210 (optional)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell us about your requirements or questions...',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        initial_topic = kwargs.pop('initial_topic', None)
        super().__init__(*args, **kwargs)

        DEFAULT_PRODUCTS = [
            ('Hospital Software / Hospital ERP', 'Product: Hospital Software / Hospital ERP'),
            ('HR Applications', 'Product: HR Applications'),
            ('Multi-module ERP', 'Product: Multi-module ERP'),
        ]

        DEFAULT_SERVICES = [
            ('Website Design & Development', 'Service: Website Design & Development'),
            ('Website Maintenance', 'Service: Website Maintenance'),
            ('Software & API Integration', 'Service: Software & API Integration'),
            ('IT Support & Application Maintenance', 'Service: IT Support & Application Maintenance'),
        ]

        choices = [
            ('', '-- Select an Option --'),
            ('General Enquiry', 'General Enquiry'),
        ]

        # Products group: load from DB with guaranteed fallback so cloud is never empty
        product_options = []
        try:
            for p in Project.objects.filter(is_active=True).order_by('order', 'id'):
                product_options.append((p.title, f"Product: {p.title}"))
        except Exception:
            pass

        if not product_options:
            product_options = list(DEFAULT_PRODUCTS)

        choices.append(('Products in Development', tuple(product_options)))

        # Services group: load from DB with guaranteed fallback so cloud is never empty
        service_options = []
        try:
            for s in Service.objects.filter(is_active=True).order_by('order', 'id'):
                service_options.append((s.title, f"Service: {s.title}"))
        except Exception:
            pass

        if not service_options:
            service_options = list(DEFAULT_SERVICES)

        choices.append(('IT Services', tuple(service_options)))

        self.fields['topic'].choices = choices

        if initial_topic:
            # Check for direct match or partial match
            initial_lower = initial_topic.strip().lower()
            selected = None
            for group_label, items in choices:
                if isinstance(items, (list, tuple)):
                    for val, label in items:
                        if val.lower() == initial_lower or initial_lower in val.lower() or val.lower() in initial_lower:
                            selected = val
                            break
                elif group_label and (group_label.lower() == initial_lower or initial_lower in group_label.lower()):
                    selected = group_label
                if selected:
                    break

            if selected:
                self.fields['topic'].initial = selected
                self.initial['topic'] = selected
            else:
                # If non-standard string, allow it by adding to choices dynamically
                choices.append(('Other', ((initial_topic, initial_topic),)))
                self.fields['topic'].choices = choices
                self.fields['topic'].initial = initial_topic
                self.initial['topic'] = initial_topic
        elif not self.is_bound:
            self.fields['topic'].initial = 'General Enquiry'
            self.initial.setdefault('topic', 'General Enquiry')
