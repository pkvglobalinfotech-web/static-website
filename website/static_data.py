"""
PKV Global Infotech — Static Site Data
========================================
All company info, products, and services are defined here as plain Python
dicts/lists. No database required. Edit this file to update the website.
"""

# ---------------------------------------------------------------------------
# COMPANY SETTINGS
# ---------------------------------------------------------------------------
COMPANY = {
    "company_name": "PKV Global Infotech Pvt Ltd",
    "headline": "Build Digital Products That Scale",
    "supporting_text": (
        "PKV Global Infotech develops hospital software, HR applications, and multi-module ERP solutions. "
        "We also help businesses build and maintain websites, connect their software systems, "
        "and get ongoing IT support."
    ),
    "email": "pkvglobalinfotech@gmail.com",
    "phone": "+91 93455 96961",
    "address": "23(1)/190, puduchery, Pennaluripeta, Tiruvallur, Tiruvallur- 602026, Tamil Nadu",
    "business_hours": "",
    "linkedin_url": "",
    "twitter_url": "",
    "github_url": "",
    "facebook_url": "",
    "instagram_url": "",
    "youtube_url": "",
}


# ---------------------------------------------------------------------------
# PRODUCTS / PROJECTS
# ---------------------------------------------------------------------------
PRODUCTS = [
    {
        "id": 1,
        "title": "Hospital Software / Hospital ERP",
        "subtitle": "Healthcare Operations & Clinical Management Suite",
        "technology": "Django, Python & PostgreSQL",
        "description": (
            "Specialised software for hospital operations and clinical care workflows, "
            "designed to streamline patient handling, medical recordkeeping, and operational billing."
        ),
        "modules": [
            "Patient Registration & Queue Scheduling (In Development)",
            "Outpatient (OP) & Inpatient (IP) Billing (In Development)",
            "Pharmacy & Medication Dispensing (In Development)",
            "Inventory & Consumables Control (In Development)",
            "Clinical Records & Doctor Notes (In Development)",
        ],
        "stage": "in_development",
        "stage_label": "In Development",
        "icon": "bi-hospital",
        "image": None,
        "github": "",
        "live_demo": "",
        "is_active": True,
        "order": 1,
    },
    {
        "id": 2,
        "title": "HR Applications",
        "subtitle": "Employee Records & Workflow Automation",
        "technology": "Python, Modern Web & Role-Based Access",
        "description": (
            "Dedicated applications for employee records and HR workflows. "
            "Built to reduce repetitive human-resource administration and standardize internal requests."
        ),
        "modules": [
            "Employee Master Records & Digital Profiles (In Development)",
            "Attendance & Leave Approval Workflows (In Development)",
            "Payroll Calculation & Payslip Export (In Development)",
            "Performance & Review Cycles (Planned)",
            "Recruitment Pipeline & Candidate Onboarding (Planned)",
        ],
        "stage": "in_development",
        "stage_label": "In Development",
        "icon": "bi-people",
        "image": None,
        "github": "",
        "live_demo": "",
        "is_active": True,
        "order": 2,
    },
    {
        "id": 3,
        "title": "Multi-module ERP",
        "subtitle": "Modular Enterprise Operations Connector",
        "technology": "Modular Architecture & Secure APIs",
        "description": (
            "Business software that connects functions such as HR, inventory, purchasing, "
            "finance, and multi-tier approvals into a unified, extensible architecture."
        ),
        "modules": [
            "Human Resources & Workforce Management (In Development)",
            "Inventory & Warehouse Stock Tracking (In Development)",
            "Purchasing & Supplier Purchase Orders (In Development)",
            "Financial Accounting & Invoicing (In Development)",
            "Multi-level Approval Workflows (In Development)",
        ],
        "stage": "in_development",
        "stage_label": "In Development",
        "icon": "bi-diagram-3",
        "image": None,
        "github": "",
        "live_demo": "",
        "is_active": True,
        "order": 3,
    },
]


# ---------------------------------------------------------------------------
# IT SERVICES
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "id": 1,
        "title": "Website Design & Development",
        "icon": "bi-laptop",
        "description": (
            "Create new company websites and business web applications tailored "
            "to your brand and technical requirements."
        ),
        "support_hours": "",
        "response_commitment": "",
        "is_active": True,
        "order": 1,
    },
    {
        "id": 2,
        "title": "Website Maintenance",
        "icon": "bi-tools",
        "description": (
            "Update content, fix issues, and maintain existing websites, "
            "including sites the customer already owns."
        ),
        "support_hours": "",
        "response_commitment": "",
        "is_active": True,
        "order": 2,
    },
    {
        "id": 3,
        "title": "Software & API Integration",
        "icon": "bi-diagram-3",
        "description": (
            "Connect existing applications, ERP modules, and third-party systems "
            "so agreed data can move smoothly between them."
        ),
        "support_hours": "",
        "response_commitment": "",
        "is_active": True,
        "order": 3,
    },
    {
        "id": 4,
        "title": "IT Support & Application Maintenance",
        "icon": "bi-headset",
        "description": (
            "Troubleshoot application issues and deliver agreed fixes and enhancements "
            "to keep your systems running reliably."
        ),
        "support_hours": "",
        "response_commitment": "",
        "is_active": True,
        "order": 4,
    },
]


# ---------------------------------------------------------------------------
# CONTACT TOPIC CHOICES  (for the enquiry form dropdown)
# ---------------------------------------------------------------------------
def get_topic_choices():
    """Return grouped choices for the Area of Interest / Topic select field."""
    product_options = tuple(
        (p["title"], f"Product: {p['title']}")
        for p in PRODUCTS
        if p["is_active"]
    )
    service_options = tuple(
        (s["title"], f"Service: {s['title']}")
        for s in SERVICES
        if s["is_active"]
    )
    return [
        ("", "-- Select an Option --"),
        ("General Enquiry", "General Enquiry"),
        ("Products in Development", product_options),
        ("IT Services", service_options),
    ]


# ---------------------------------------------------------------------------
# HELPER: get active products / services (mirrors ORM-style interface)
# ---------------------------------------------------------------------------
def get_active_products():
    return [p for p in PRODUCTS if p["is_active"]]


def get_active_services():
    return [s for s in SERVICES if s["is_active"]]
