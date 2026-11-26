"""
PKV Global Infotech — Test Suite (database-free architecture)
=============================================================
All site data comes from website/static_data.py.
Contact submissions are email-only (no DB records).
"""
from django.test import TestCase, Client, override_settings
from django.conf import settings
from unittest.mock import patch, MagicMock

from website.forms import ContactForm
from website.static_data import (
    COMPANY, PRODUCTS, SERVICES,
    get_active_products, get_active_services, get_topic_choices,
)


# ---------------------------------------------------------------------------
# Static Data Tests
# ---------------------------------------------------------------------------

class StaticDataTests(TestCase):
    """Verify static_data.py exports the right shape of data."""

    def test_company_has_required_keys(self):
        for key in ("company_name", "headline", "email", "phone", "address"):
            self.assertIn(key, COMPANY, f"COMPANY missing key: {key}")

    def test_products_non_empty(self):
        products = get_active_products()
        self.assertGreater(len(products), 0, "get_active_products() returned empty list")

    def test_services_non_empty(self):
        services = get_active_services()
        self.assertGreater(len(services), 0, "get_active_services() returned empty list")

    def test_product_has_required_keys(self):
        for p in PRODUCTS:
            for key in ("title", "description", "modules", "stage", "stage_label", "is_active"):
                self.assertIn(key, p, f"Product '{p.get('title')}' missing key: {key}")
            self.assertIsInstance(p["modules"], list, "modules should be a list")

    def test_service_has_required_keys(self):
        for s in SERVICES:
            for key in ("title", "description", "icon", "is_active"):
                self.assertIn(key, s, f"Service '{s.get('title')}' missing key: {key}")

    def test_company_headline(self):
        self.assertEqual(COMPANY["headline"], "Build Digital Products That Scale")

    def test_company_phone(self):
        self.assertEqual(COMPANY["phone"], "+91 93455 96961")

    def test_company_address_contains_tiruvallur(self):
        self.assertIn("Tiruvallur", COMPANY["address"])

    def test_company_email(self):
        self.assertEqual(COMPANY["email"], "pkvglobalinfotech@gmail.com")


# ---------------------------------------------------------------------------
# Topic Choices Tests
# ---------------------------------------------------------------------------

class TopicChoicesTests(TestCase):
    """Verify the contact form topic dropdown has all expected options."""

    def test_dropdown_has_general_enquiry(self):
        choices = get_topic_choices()
        all_vals = []
        for group, items in choices:
            if isinstance(items, (list, tuple)):
                for val, _ in items:
                    all_vals.append(val)
            else:
                all_vals.append(group)
        self.assertIn("General Enquiry", all_vals)

    def test_dropdown_has_all_product_groups(self):
        choices = get_topic_choices()
        groups = [g for g, _ in choices]
        self.assertIn("Software Products", groups)
        self.assertIn("IT Services", groups)

    def test_dropdown_has_hospital_product(self):
        choices = get_topic_choices()
        all_vals = [v for _, items in choices if isinstance(items, (list, tuple)) for v, _ in items]
        self.assertIn("Hospital Software / Hospital ERP", all_vals)

    def test_dropdown_has_all_services(self):
        choices = get_topic_choices()
        service_vals = []
        for group, items in choices:
            if group == "IT Services":
                service_vals = [v for v, _ in items]
        self.assertIn("Website Design & Development", service_vals)
        self.assertIn("Website Maintenance", service_vals)
        self.assertIn("Software & API Integration", service_vals)
        self.assertIn("IT Support & Application Maintenance", service_vals)


# ---------------------------------------------------------------------------
# Contact Form Tests
# ---------------------------------------------------------------------------

class ContactFormTests(TestCase):
    """Verify ContactForm validation and initial selection."""

    def test_valid_form(self):
        form = ContactForm(data={
            'topic': 'General Enquiry',
            'name': 'Test User',
            'company_name': 'Acme Healthcare Ltd',
            'email': 'test@example.com',
            'phone': '+91 99999 00000',
            'message': 'Hello, I need a website.',
        })
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['company_name'], 'Acme Healthcare Ltd')

    def test_invalid_without_required_fields(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('message', form.errors)

    def test_invalid_email(self):
        form = ContactForm(data={
            'topic': 'General Enquiry',
            'name': 'Test User',
            'email': 'not-an-email',
            'message': 'Test message',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_initial_topic_preselection(self):
        form = ContactForm(initial_topic='HR Applications')
        self.assertEqual(form.initial.get('topic'), 'HR Applications')

    def test_default_topic_is_general_enquiry(self):
        form = ContactForm()
        self.assertEqual(form.initial.get('topic'), 'General Enquiry')

    def test_dropdown_widget_contains_all_options(self):
        form = ContactForm()
        html = form['topic'].as_widget()
        self.assertIn('General Enquiry', html)
        self.assertIn('Hospital Software / Hospital ERP', html)
        self.assertIn('HR Applications', html)
        self.assertIn('Multi-module ERP', html)
        self.assertIn('Website Maintenance', html)


# ---------------------------------------------------------------------------
# View / URL Tests
# ---------------------------------------------------------------------------

@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.dummy.EmailBackend',
)
class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    # Pages load OK
    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Build Digital Products That Scale")

    def test_products_page_loads(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hospital Software")

    def test_services_page_loads(self):
        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Website Design")

    def test_contact_page_loads(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Area of Interest")

    def test_about_page_loads(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    # Contact form submission
    def test_contact_form_valid_submission_redirects(self):
        with patch('website.views.threading.Thread') as mock_thread:
            mock_thread.return_value = MagicMock()
            mock_thread.return_value.start = MagicMock()

            response = self.client.post('/contact/', {
                'topic': 'General Enquiry',
                'name': 'PKV Test',
                'email': 'pkv@example.com',
                'phone': '+91 90000 00000',
                'message': 'Please get in touch.',
            })
            self.assertRedirects(response, '/contact/')

    def test_contact_form_invalid_does_not_redirect(self):
        response = self.client.post('/contact/', {
            'topic': '',
            'name': '',
            'email': 'bad-email',
            'message': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_contact_success_message_shown(self):
        with patch('website.views.threading.Thread') as mock_thread:
            mock_thread.return_value = MagicMock()
            mock_thread.return_value.start = MagicMock()

            response = self.client.post('/contact/', {
                'topic': 'General Enquiry',
                'name': 'PKV Test',
                'email': 'pkv@example.com',
                'message': 'Please get in touch.',
            }, follow=True)
            self.assertContains(response, "Thank you! Your enquiry has been received.")
