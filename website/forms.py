from django import forms
from .static_data import get_topic_choices


class ContactForm(forms.Form):
    """
    Enquiry form — no database model required.
    All validation is done in-memory; submission is dispatched via email only.
    """

    topic = forms.ChoiceField(
        choices=[],                      # populated dynamically in __init__
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Area of Interest / Topic",
        help_text="Select a specific product, IT service, or general enquiry",
    )
    name = forms.CharField(
        max_length=100,
        label="Full Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name',
            'required': True,
        }),
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'you@company.com',
            'required': True,
        }),
    )
    phone = forms.CharField(
        max_length=30,
        required=False,
        label="Contact Phone (optional)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+91 98765 43210 (optional)',
        }),
    )
    message = forms.CharField(
        label="Requirement Details",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Tell us about your requirements or questions...',
            'required': True,
        }),
    )

    def __init__(self, *args, **kwargs):
        initial_topic = kwargs.pop('initial_topic', None)
        super().__init__(*args, **kwargs)

        choices = get_topic_choices()
        self.fields['topic'].choices = choices

        # Pre-select a topic if passed via URL param
        if initial_topic:
            initial_lower = initial_topic.strip().lower()
            selected = None
            for group_or_val, items in choices:
                if isinstance(items, (list, tuple)):
                    for val, label in items:
                        if (val.lower() == initial_lower
                                or initial_lower in val.lower()
                                or val.lower() in initial_lower):
                            selected = val
                            break
                elif group_or_val and (
                    group_or_val.lower() == initial_lower
                    or initial_lower in group_or_val.lower()
                ):
                    selected = group_or_val
                if selected:
                    break

            if selected:
                self.initial['topic'] = selected
            else:
                # Unknown topic → add as free-text option
                choices.append(('Other', ((initial_topic, initial_topic),)))
                self.fields['topic'].choices = choices
                self.initial['topic'] = initial_topic
        elif not self.is_bound:
            self.initial.setdefault('topic', 'General Enquiry')
