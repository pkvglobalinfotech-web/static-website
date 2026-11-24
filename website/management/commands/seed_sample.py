from django.core.management.base import BaseCommand
from website.models import CompanySetting, Service, Project


class Command(BaseCommand):
    help = 'Create PKV Global Infotech default products, services, and company settings if not already present. Preserves staff edits on re-run.'

    def add_arguments(self, parser):
        parser.add_argument('--create', action='store_true', help='Seed initial company data, products, and services without overwriting staff edits')
        parser.add_argument('--clear', action='store_true', help='Clear sample products and services (destructive)')

    def handle(self, *args, **options):
        if options['clear']:
            Project.objects.all().delete()
            Service.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared products and services.'))
            return

        # 1. Company Settings: create default only if none exists; preserve staff edits
        company = CompanySetting.objects.first()
        if not company:
            company = CompanySetting.objects.create(
                company_name="PKV Global Infotech Pvt Ltd",
                headline="Build Digital Products That Scale",
                supporting_text=(
                    "PKV Global Infotech develops hospital software, HR applications, and multi-module ERP solutions. "
                    "We also help businesses build and maintain websites, connect their software systems, and get ongoing IT support."
                ),
                email="pkvglobalinfotech@gmail.com",
                phone="+91 93455 96961",
                address="23(1)/190, puduchery, Pennaluripeta, Tiruvallur, Tiruvallur- 602026, Tamil Nadu",
                business_hours="",
            )
            self.stdout.write(self.style.SUCCESS('Created default Company Settings.'))
        else:
            self.stdout.write(self.style.NOTICE('Company Settings already exist; preserving staff edits.'))

        # 2. Products: all unconfirmed capabilities set to 'In Development'
        products_data = [
            {
                'title': 'Hospital Software / Hospital ERP',
                'subtitle': 'Healthcare Operations & Clinical Management Suite',
                'technology': 'Django, Python & PostgreSQL',
                'description': (
                    'Specialised software for hospital operations and clinical care workflows, '
                    'designed to streamline patient handling, medical recordkeeping, and operational billing.'
                ),
                'modules': (
                    'Patient Registration & Queue Scheduling (In Development)\n'
                    'Outpatient (OP) & Inpatient (IP) Billing (In Development)\n'
                    'Pharmacy & Medication Dispensing (In Development)\n'
                    'Inventory & Consumables Control (In Development)\n'
                    'Clinical Records & Doctor Notes (In Development)'
                ),
                'stage': 'in_development',
                'order': 1,
                'is_active': True,
                'live_demo': '',
            },
            {
                'title': 'HR Applications',
                'subtitle': 'Employee Records & Workflow Automation',
                'technology': 'Python, Modern Web & Role-Based Access',
                'description': (
                    'Dedicated applications for employee records and HR workflows. '
                    'Built to reduce repetitive human-resource administration and standardize internal requests.'
                ),
                'modules': (
                    'Employee Master Records & Digital Profiles (In Development)\n'
                    'Attendance & Leave Approval Workflows (In Development)\n'
                    'Payroll Calculation & Payslip Export (In Development)\n'
                    'Performance & Review Cycles (Planned)\n'
                    'Recruitment Pipeline & Candidate Onboarding (Planned)'
                ),
                'stage': 'in_development',
                'order': 2,
                'is_active': True,
                'live_demo': '',
            },
            {
                'title': 'Multi-module ERP',
                'subtitle': 'Modular Enterprise Operations Connector',
                'technology': 'Modular Architecture & Secure APIs',
                'description': (
                    'Business software that connects functions such as HR, inventory, purchasing, '
                    'finance, and multi-tier approvals into a unified, extensible architecture.'
                ),
                'modules': (
                    'Human Resources & Workforce Management (In Development)\n'
                    'Inventory & Warehouse Stock Tracking (In Development)\n'
                    'Purchasing & Supplier Purchase Orders (In Development)\n'
                    'Financial Accounting & Invoicing (In Development)\n'
                    'Multi-level Approval Workflows (In Development)'
                ),
                'stage': 'in_development',
                'order': 3,
                'is_active': True,
                'live_demo': '',
            },
        ]

        for p_data in products_data:
            obj, created = Project.objects.get_or_create(
                title=p_data['title'],
                defaults=p_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {obj.title}'))
            else:
                self.stdout.write(self.style.NOTICE(f'Product already exists; preserving staff edits: {obj.title}'))

        # 3. IT Services: create if not existing; preserve staff edits
        services_data = [
            {
                'title': 'Website Design & Development',
                'icon': 'bi-laptop',
                'description': 'Create new company websites and business web applications tailored to your brand and technical requirements.',
                'support_hours': '',
                'response_commitment': '',
                'order': 1,
                'is_active': True,
            },
            {
                'title': 'Website Maintenance',
                'icon': 'bi-tools',
                'description': 'Update content, fix issues, and maintain existing websites, including sites the customer already owns.',
                'support_hours': '',
                'response_commitment': '',
                'order': 2,
                'is_active': True,
            },
            {
                'title': 'Software & API Integration',
                'icon': 'bi-diagram-3',
                'description': 'Connect existing applications, ERP modules, and third-party systems so agreed data can move smoothly between them.',
                'support_hours': '',
                'response_commitment': '',
                'order': 3,
                'is_active': True,
            },
            {
                'title': 'IT Support & Application Maintenance',
                'icon': 'bi-headset',
                'description': 'Troubleshoot application issues and deliver agreed fixes and enhancements to keep your systems running reliably.',
                'support_hours': '',
                'response_commitment': '',
                'order': 4,
                'is_active': True,
            },
        ]

        for s_data in services_data:
            obj, created = Service.objects.get_or_create(
                title=s_data['title'],
                defaults=s_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created service: {obj.title}'))
            else:
                self.stdout.write(self.style.NOTICE(f'Service already exists; preserving staff edits: {obj.title}'))

        self.stdout.write(self.style.SUCCESS('PKV Global Infotech seed check completed.'))
