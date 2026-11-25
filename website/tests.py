from django.test import TestCase, Client, override_settings
from django.conf import settings
from django.core import mail
from django.core.management import call_command
from django.contrib.auth.models import User
from website.models import Service, Project, Contact, CompanySetting
from website.forms import ContactForm
from unittest.mock import patch


@override_settings(PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher'])
class WebsiteTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Company settings
        self.company = CompanySetting.get_settings()
        self.company.company_name = "PKV Global Infotech Pvt Ltd"
        self.company.headline = "Build Digital Products That Scale"
        self.company.supporting_text = (
            "PKV Global Infotech develops hospital software, HR applications, and multi-module ERP solutions. "
            "We also help businesses build and maintain websites, connect their software systems, and get ongoing IT support."
        )
        self.company.email = "pkvglobalinfotech@gmail.com"
        self.company.phone = "+91 93455 96961"
        self.company.address = "23(1)/190, puduchery, Pennaluripeta, Tiruvallur, Tiruvallur- 602026, Tamil Nadu"
        self.company.business_hours = ""
        self.company.save()

        # Seed 3 products
        self.hospital_product = Project.objects.create(
            title="Hospital Software / Hospital ERP",
            subtitle="Healthcare Operations & Clinical Management Suite",
            technology="Django & PostgreSQL",
            description="Dedicated software for hospital operations.",
            modules="Patient Registration & Queue Scheduling (In Development)\nOP/IP Billing (In Development)\nPharmacy & Inventory (In Development)\nClinical Records (In Development)",
            stage="in_development",
            order=1,
            is_active=True,
        )
        self.hr_product = Project.objects.create(
            title="HR Applications",
            subtitle="Employee Records & Workflows",
            technology="Python & Modern Web",
            description="Applications for employee records and HR workflows.",
            modules="Employee Master Records (In Development)\nAttendance & Leave Management (In Development)\nPayroll Calculation (In Development)",
            stage="in_development",
            order=2,
            is_active=True,
        )
        self.erp_product = Project.objects.create(
            title="Multi-module ERP",
            subtitle="Business Operations Suite",
            technology="Modular Django",
            description="Business software connecting HR, inventory, purchasing, finance, and approvals.",
            modules="HR & Workforce (In Development)\nInventory & Warehouse (In Development)\nPurchasing & Orders (In Development)\nFinance & Invoicing (In Development)",
            stage="in_development",
            order=3,
            is_active=True,
        )

        # Seed 4 services
        self.service_web = Service.objects.create(
            title="Website Design & Development",
            icon="bi-laptop",
            description="Create new company websites and business web applications.",
            order=1,
            is_active=True,
        )
        self.service_maint = Service.objects.create(
            title="Website Maintenance",
            icon="bi-tools",
            description="Update content, fix issues, and maintain existing websites, including sites the customer already owns.",
            order=2,
            is_active=True,
        )
        self.service_integ = Service.objects.create(
            title="Software & API Integration",
            icon="bi-diagram-3",
            description="Connect existing applications, ERP modules, and third-party systems so agreed data can move between them.",
            order=3,
            is_active=True,
        )
        self.service_supp = Service.objects.create(
            title="IT Support & Application Maintenance",
            icon="bi-headset",
            description="Troubleshoot application issues and deliver agreed fixes and enhancements.",
            order=4,
            is_active=True,
        )

        # Admin superuser
        self.admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='testpassword123'
        )

    def test_homepage_structure_and_wording(self):
        """Verify homepage contains required headline, exact supporting text, buttons, and removes ungrounded claims."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Main heading
        self.assertContains(response, "Build Digital Products That Scale")

        # Supporting text
        self.assertContains(
            response,
            "PKV Global Infotech develops hospital software, HR applications, and multi-module ERP solutions. "
            "We also help businesses build and maintain websites, connect their software systems, and get ongoing IT support."
        )

        # Two primary buttons
        self.assertContains(response, "Explore Products")
        self.assertContains(response, "Discuss Your Requirement")

        content = response.content.decode('utf-8')
        hero_pos = content.find("Build Digital Products That Scale")
        products_pos = content.find('id="products"')
        services_pos = content.find('id="services"')
        contact_pos = content.find('Send an Enquiry')

        self.assertTrue(hero_pos < products_pos < services_pos < contact_pos)

        # Ensure unsupported claims and placeholders are removed
        self.assertNotIn("150+ Projects", content)
        self.assertNotIn("50+ Satisfied Clients", content)
        self.assertNotIn("10 Awards", content)
        self.assertNotIn("24/7 Support", content)
        self.assertNotIn("+91 90000 00000", content)
        self.assertNotIn("Client Reviews", content)
        self.assertNotIn("David Willson", content)

    def test_products_catalog_and_urls(self):
        """Verify both /products/ and /portfolio/ URLs work and render products with stage and modules."""
        for url in ['/products/', '/portfolio/']:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

            self.assertContains(response, "Hospital Software / Hospital ERP")
            self.assertContains(response, "HR Applications")
            self.assertContains(response, "Multi-module ERP")
            self.assertContains(response, "In Development")
            self.assertContains(response, "Enquire About This Product")
            self.assertNotContains(response, "View Demo")

    def test_services_catalog_and_enquiry_buttons(self):
        """Verify /services/ lists all 4 offerings with enquiry buttons."""
        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Website Design &amp; Development")
        self.assertContains(response, "Website Maintenance")
        self.assertContains(response, "Software &amp; API Integration")
        self.assertContains(response, "IT Support &amp; Application Maintenance")
        self.assertContains(response, "Enquire About This Service")

    def test_visitor_journey_1_hospital_erp_and_reply_to(self):
        """
        Visitor Journey 1:
        Hospital visitor selects Hospital ERP, submits enquiry.
        Verify sender, recipient, visitor Reply-To header, persistence, and Admin display.
        """
        contact_url = f"/contact/?topic={self.hospital_product.title}"
        response = self.client.get(contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'selected>Product: Hospital Software / Hospital ERP</option>')

        mail.outbox.clear()
        post_data = {
            'topic': self.hospital_product.title,
            'name': 'City General Hospital',
            'email': 'admin@cityhospital.example',
            'phone': '+91 98401 23456',
            'message': 'We are looking for an integrated OP/IP billing and pharmacy software for our 120-bed hospital.',
        }
        submit_response = self.client.post('/contact/', post_data, follow=True)
        self.assertEqual(submit_response.status_code, 200)
        self.assertContains(submit_response, 'Your enquiry has been received')

        # Database record
        enquiry = Contact.objects.filter(email='admin@cityhospital.example').first()
        self.assertIsNotNone(enquiry)
        self.assertEqual(enquiry.topic, 'Hospital Software / Hospital ERP')
        self.assertEqual(enquiry.name, 'City General Hospital')
        self.assertEqual(enquiry.status, 'new')
        self.assertTrue(enquiry.email_sent)

        # Email dispatch verification: Configured sender, monitored inbox, visitor Reply-To, and auto-reply
        self.assertEqual(len(mail.outbox), 2)
        sent_email = mail.outbox[0]
        self.assertIn("Hospital Software / Hospital ERP", sent_email.subject)
        self.assertEqual(sent_email.to, ['pkvglobalinfotech@gmail.com'])
        self.assertEqual(sent_email.reply_to, ['admin@cityhospital.example'])
        self.assertEqual(sent_email.from_email, settings.DEFAULT_FROM_EMAIL)

        ack_email = mail.outbox[1]
        self.assertIn("Thank you for contacting PKV Global Infotech", ack_email.subject)
        self.assertEqual(ack_email.to, ['admin@cityhospital.example'])
        self.assertIn("City General Hospital", ack_email.body)
        self.assertIn("reply to you shortly", ack_email.body)

        # Admin display
        self.client.force_login(self.admin_user)
        admin_response = self.client.get('/admin/website/contact/')
        self.assertEqual(admin_response.status_code, 200)
        self.assertContains(admin_response, 'City General Hospital')
        self.assertContains(admin_response, 'Accepted by Backend')

    def test_visitor_journey_2_website_maintenance_and_reply_to(self):
        """
        Visitor Journey 2:
        Business selects Website Maintenance, submits enquiry.
        Verify reply-to header, persistence, and Admin display.
        """
        contact_url = f"/contact/?topic={self.service_maint.title}"
        response = self.client.get(contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'selected>Service: Website Maintenance</option>')

        mail.outbox.clear()
        post_data = {
            'topic': self.service_maint.title,
            'name': 'Apex Retailers',
            'email': 'support@apexretailers.example',
            'phone': '+91 99000 11223',
            'message': 'We need ongoing monthly maintenance and security patching for our existing sites.',
        }
        submit_response = self.client.post('/contact/', post_data, follow=True)
        self.assertEqual(submit_response.status_code, 200)

        enquiry = Contact.objects.filter(email='support@apexretailers.example').first()
        self.assertIsNotNone(enquiry)
        self.assertTrue(enquiry.email_sent)

        self.assertEqual(len(mail.outbox), 2)
        sent_email = mail.outbox[0]
        self.assertIn("Website Maintenance", sent_email.subject)
        self.assertEqual(sent_email.to, ['pkvglobalinfotech@gmail.com'])
        self.assertEqual(sent_email.reply_to, ['support@apexretailers.example'])

        ack_email = mail.outbox[1]
        self.assertIn("Thank you for contacting PKV Global Infotech", ack_email.subject)
        self.assertEqual(ack_email.to, ['support@apexretailers.example'])

        self.client.force_login(self.admin_user)
        admin_response = self.client.get('/admin/website/contact/')
        self.assertContains(admin_response, 'Apex Retailers')
        self.assertContains(admin_response, 'Accepted by Backend')

    def test_contact_privacy_terms_footer_contact_consistency(self):
        """
        Confirm Contact, Privacy, Terms, and footer share same company contact details
        and contain NO placeholder phone numbers (+91 XXXXX XXXXX) or unconfirmed response promises (within 48 hours).
        """
        pages = ['/contact/', '/privacy-policy/', '/terms-and-conditions/', '/about/']
        for url in pages:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            content = response.content.decode('utf-8')

            # Official email, phone, and address used consistently
            self.assertIn('pkvglobalinfotech@gmail.com', content)
            self.assertIn('+91 93455 96961', content)
            self.assertIn('23(1)/190, puduchery, Pennaluripeta, Tiruvallur, Tiruvallur- 602026, Tamil Nadu', content)

            # No placeholder phone numbers
            self.assertNotIn('+91 XXXXX XXXXX', content)
            self.assertNotIn('+91 90000 00000', content)

            # No unconfirmed response promises
            self.assertNotIn('within 48 hours', content)
            self.assertNotIn('within 1-2 business days', content)

    def test_seed_command_idempotence_and_preserves_edits(self):
        """
        Verify that running seed_sample command twice preserves staff edits
        without creating duplicate products, services, or settings.
        """
        # Run 1: seed initially
        call_command('seed_sample', create=True)
        initial_prod_count = Project.objects.count()
        initial_serv_count = Service.objects.count()
        initial_comp_count = CompanySetting.objects.count()

        # Simulate staff edits in Django Admin
        h_prod = Project.objects.filter(title__contains='Hospital').first()
        h_prod.description = "Staff customized clinical description."
        h_prod.stage = "ready_to_demo"
        h_prod.save()

        m_serv = Service.objects.filter(title='Website Maintenance').first()
        m_serv.description = "Staff customized maintenance terms."
        m_serv.save()

        comp = CompanySetting.get_settings()
        comp.phone = "+91 44 2800 1234"
        comp.save()

        # Run 2: re-run seed command
        call_command('seed_sample', create=True)

        # Check counts: NO DUPLICATES
        self.assertEqual(Project.objects.count(), initial_prod_count)
        self.assertEqual(Service.objects.count(), initial_serv_count)
        self.assertEqual(CompanySetting.objects.count(), initial_comp_count)

        # Check staff edits: PRESERVED
        h_prod.refresh_from_db()
        self.assertEqual(h_prod.description, "Staff customized clinical description.")
        self.assertEqual(h_prod.stage, "ready_to_demo")

        m_serv.refresh_from_db()
        self.assertEqual(m_serv.description, "Staff customized maintenance terms.")

        comp.refresh_from_db()
        self.assertEqual(comp.phone, "+91 44 2800 1234")

    def test_admin_updates_propagate_to_public_pages(self):
        """Verify admin edits propagate immediately to public pages."""
        self.hospital_product.stage = 'ready_to_demo'
        self.hospital_product.live_demo = 'https://demo.hospital.pkvglobalinfotech.com'
        self.hospital_product.save()

        response = self.client.get('/products/')
        self.assertContains(response, "Ready to Demonstrate")
        self.assertContains(response, "View Demo")
        self.assertContains(response, "https://demo.hospital.pkvglobalinfotech.com")

    def test_email_failure_resilience(self):
        """Verify SMTP failure records email_sent=False without losing enquiry."""
        with patch('django.core.mail.EmailMessage.send', side_effect=Exception('SMTP Connection Refused')):
            post_data = {
                'topic': 'General Enquiry',
                'name': 'Test User',
                'email': 'testuser@example.com',
                'phone': '+91 12345 67890',
                'message': 'Testing error handling.',
            }
            response = self.client.post('/contact/', post_data, follow=True)
            self.assertEqual(response.status_code, 200)

            enquiry = Contact.objects.filter(email='testuser@example.com').first()
            self.assertIsNotNone(enquiry)
            self.assertFalse(enquiry.email_sent)
            self.assertIn('SMTP Connection Refused', enquiry.email_error)

    def test_prevent_duplicate_submissions_at_same_time(self):
        """Verify submitting the same enquiry within 60 seconds is rejected and deduplicated."""
        post_data = {
            'topic': 'General Enquiry',
            'name': 'Duplicate Tester',
            'email': 'duplicate@example.com',
            'phone': '+91 99999 88888',
            'message': 'Submitting once then rapidly again.',
        }
        # First submission succeeds
        res1 = self.client.post('/contact/', post_data, follow=True)
        self.assertEqual(res1.status_code, 200)
        self.assertContains(res1, "Thank you! Your enquiry has been received.")

        initial_count = Contact.objects.filter(email='duplicate@example.com').count()
        self.assertEqual(initial_count, 1)

        # Immediate second submission is caught and prevented
        res2 = self.client.post('/contact/', post_data, follow=True)
        self.assertEqual(res2.status_code, 200)
        self.assertContains(res2, "Your enquiry has already been received")

        # Database record count remains 1 (no duplicate record created)
        after_count = Contact.objects.filter(email='duplicate@example.com').count()
        self.assertEqual(after_count, 1)

    def test_contact_form_dropdown_options_fallback_when_db_empty(self):
        """
        Verify that ContactForm provides default options for products and services
        even when the database has 0 products and 0 services (common on fresh cloud deploys).
        """
        Project.objects.all().delete()
        Service.objects.all().delete()

        form = ContactForm()
        widget_html = form['topic'].as_widget()

        self.assertIn('General Enquiry', widget_html)
        self.assertIn('Products in Development', widget_html)
        self.assertIn('Hospital Software / Hospital ERP', widget_html)
        self.assertIn('HR Applications', widget_html)
        self.assertIn('Multi-module ERP', widget_html)
        self.assertIn('IT Services', widget_html)
        self.assertIn('Website Design &amp; Development', widget_html)
        self.assertIn('Website Maintenance', widget_html)
        self.assertIn('Software &amp; API Integration', widget_html)
        self.assertIn('IT Support &amp; Application Maintenance', widget_html)

    def test_lazy_seed_catalog_populates_empty_database(self):
        """
        Verify that _ensure_catalog_seeded() populates Project and Service
        tables when they are empty, ensuring cloud pages are never blank.
        """
        Project.objects.all().delete()
        Service.objects.all().delete()
        self.assertEqual(Project.objects.count(), 0)
        self.assertEqual(Service.objects.count(), 0)

        # Call seed_sample --create to simulate lazy seeding
        call_command('seed_sample', create=True)

        self.assertEqual(Project.objects.count(), 3)
        self.assertEqual(Service.objects.count(), 4)


