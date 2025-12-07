## RetailCurbside Architecture

### Stack
- Django 5 monolith with modular `apps/` packages for users, inventory, orders, and curbside orchestration.
- Tailwind via CDN + Alpine.js for micro-interactions; HTMX handles cart badge refreshes, arrival check-ins, and staff dashboard polling.
- Channels ready (HTTP + websocket ASGI router). Dev defaults to in-memory channels via env flag; production expects Redis.
- Celery configured (broker defaults to Redis) for future async order processing hooks.

### App Responsibilities
- `apps.users`: Custom `User` model with role enum (`customer`, `staff`, `manager`). Provides auth views (login, signup, profile) and `StaffRequiredMixin`.
- `apps.inventory`: Category + Product catalog, search/filter list + detail views.
- `apps.orders`: Session cart helper, checkout form, order + order items, customer dashboards, and staff status endpoint. Business logic isolated in `services.py`.
- `apps.curbside`: Pickup slot capacity planning, arrival alerts, staff dashboard HTMX stream, and auto-slot seeding service (`ensure_default_pickup_slots`).

### Key Flows
1. **Catalog** - Public view served by `CatalogView`; HTMX-powered add-to-cart buttons keep the global badge synced.
2. **Checkout** - Auth-required; form enforces available pickup slots. Service layer validates stock, decrements inventory, and ties slot capacity.
3. **Arrival** - Customers on a ready order submit vehicle/spot via HTMX, which creates the `ArrivalAlert` and bumps order status -> `customer_arrived`.
4. **Staff Portal** - `/staff/dashboard/` polls the streamlined orders partial every 5 seconds. Inline HTMX forms toggle statuses to "Ready" or "Completed" without reloads.

### Settings
- `config/settings/base.py` provides the shared config, `.env` parsing, static directories, context processors, custom user, and Channels/Celery defaults.
- `dev.py` enables debug conveniences and optional in-memory channel layer.
- `prod.py` hardens cookies + static storage.

### Data Bootstrapping
- Run `python manage.py createsuperuser` to seed staff/manager accounts.
- Use admin to upload Categories/Products.
- Pickup slots auto-provision on first checkout attempt (`apps.curbside.services.ensure_default_pickup_slots`). Adjust timing/capacity via env/command if needed.
