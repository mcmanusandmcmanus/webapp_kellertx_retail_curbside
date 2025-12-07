## RetailCurbside

Click-and-collect curbside ordering experience for CBD retail operations. Built with Django 5, Tailwind, HTMX and Alpine.js.

### Features
- Product catalog with search/filtering and session cart.
- Checkout workflow with pickup slot selection and automated slot generation.
- Customer order dashboard with curbside arrival button.
- Staff portal with live HTMX refresh, status actions, and arrival context.
- Custom user accounts with customer/staff roles.

### Local Setup
1. `python -m venv .venv && .venv\Scripts\activate`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and adjust secrets. By default `USE_INMEMORY_CHANNEL_LAYER=True` skips Redis for dev.
4. `python manage.py migrate`
5. `python manage.py createsuperuser`
6. `python manage.py runserver`

Use the Admin (`/admin/`) to load Categories/Products or craft fixtures. Pickup slots auto-seed during checkout, but you can also create them via admin.
