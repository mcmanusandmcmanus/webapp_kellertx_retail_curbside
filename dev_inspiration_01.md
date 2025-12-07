


Here is a comprehensive technical specification formatted in Markdown (`.md`). You can save this file as `PROJECT_SPEC.md` or `ARCHITECTURE.md` in your workspace and reference it when prompting VS Code Codex or GitHub Copilot to ensure context-aware code generation.

-----

````markdown
# Project Specification: Django Curbside Pickup Application

## 1. Project Overview
**App Name:** RetailCurbside
**Type:** Monolithic Full-Stack Django Application
**Goal:** A retail e-commerce platform focusing on "Click and Collect" workflows.
**Core Workflow:** Customer orders online -> Selects pickup slot -> Staff prepares order -> Customer arrives & checks in (via app) -> Staff delivers to car.

## 2. Technology Stack
* **Backend:** Python 3.12+, Django 5.x
* **Database:** PostgreSQL (Production), SQLite (Dev)
* **Frontend:** Django Templates (Jinja2 syntax)
* **Interactivity:** HTMX (for AJAX/Swap interactions), Alpine.js (for light UI state)
* **Styling:** Tailwind CSS (via CDN or npm build process)
* **Async/Real-time:** Django Channels + Redis (for live staff dashboard updates)
* **Task Queue:** Celery + Redis (for order processing, emails)

## 3. Directory Structure
Adhere strictly to a modular "Apps" structure to separate concerns.

```text
/retail_curbside_root
├── /config                 # Project settings and configuration
│   ├── settings/
│   │   ├── base.py         # Shared settings
│   │   ├── dev.py          # Local development overrides
│   │   └── prod.py         # Production settings
│   ├── asgi.py             # For Channels/WebSocket support
│   └── urls.py             # Main URL routing
├── /apps                   # Domain-specific logic
│   ├── /users              # Custom User Model, Auth
│   ├── /inventory          # Products, Categories, Stock
│   ├── /orders             # Cart, Order Management, Payments
│   └── /curbside           # Pickup logic, Check-in, Staff Dashboard
├── /static                 # Global static files (CSS/JS/Images)
├── /templates              # Global templates (base.html, navbar.html)
├── .env                    # Environment variables (NOT commited)
├── manage.py
└── requirements.txt
````

## 4\. Database Schema & Models

### A. App: `apps.users`

  * **Model: `User`** (AbstractUser)
      * `type`: ChoiceField (Customer, Staff, Manager)
      * `phone_number`: CharField

### B. App: `apps.inventory`

  * **Model: `Category`**
      * `name`, `slug`
  * **Model: `Product`**
      * `name`, `sku`, `price`, `stock_quantity`, `image`
      * `is_active`: Boolean

### C. App: `apps.orders`

  * **Model: `Order`**
      * `user`: FK to User
      * `status`: ChoiceField (Pending, Processing, Ready\_For\_Pickup, Customer\_Arrived, Completed, Cancelled)
      * `total_amount`: Decimal
      * `created_at`: DateTime
  * **Model: `OrderItem`**
      * `order`: FK to Order
      * `product`: FK to Product
      * `quantity`: Integer

### D. App: `apps.curbside`

  * **Model: `PickupSlot`**
      * `start_time`: DateTime
      * `end_time`: DateTime
      * `max_orders`: Integer (Capacity planning)
  * **Model: `ArrivalAlert`**
      * `order`: OneToOneField to Order
      * `vehicle_desc`: CharField (e.g., "Blue Ford F-150")
      * `parking_spot`: CharField (e.g., "Spot 4")
      * `arrived_at`: DateTime (auto\_now\_add)

## 5\. Functional Requirements & Logic

### Customer Flow (Frontend)

1.  **Catalog:** User browses products and adds to session-based cart.
2.  **Checkout:** User selects a `PickupSlot` during checkout.
3.  **Dashboard:** User sees order list. If status is `Ready_For_Pickup`, a "I'm Here" button appears.
4.  **Check-in:** Clicking "I'm Here" triggers an HTMX POST request to create an `ArrivalAlert`.

### Staff Flow (Dashboard)

1.  **Live View:** A dashboard that polls (or uses WebSockets) for orders with status `Ready_For_Pickup` or `Customer_Arrived`.
2.  **Visual Cues:**
      * Status `Customer_Arrived` highlights the row in **RED** or **GREEN**.
      * Displays Vehicle Description and Parking Spot.
3.  **Action:** Staff clicks "Complete Order" to mark status as `Completed`.

## 6\. Coding Standards & Patterns

  * **Fat Models, Thin Views:** Put business logic (e.g., calculating totals, checking stock) in `models.py` methods or `services.py`, not in `views.py`.
  * **Class-Based Views (CBVs):** Use Django's generic CBVs (`ListView`, `DetailView`, `CreateView`) where possible.
  * **HTMX Integration:**
      * Do not write full page reloads for simple state changes (like updating cart count).
      * Return partial HTML templates for HTMX requests.
  * **Security:**
      * Use `django-environ` for secret management.
      * Ensure all Views have `@login_required` or `LoginRequiredMixin` where appropriate.

## 7\. Implementation Roadmap

1.  **Phase 1:** Setup Django project, Custom User model, and basic Auth.
2.  **Phase 2:** Inventory and Product catalog views.
3.  **Phase 3:** Shopping Cart (Sessions) and Checkout (Order creation).
4.  **Phase 4:** Curbside logic: Pickup Slots and "I'm Here" functionality.
5.  **Phase 5:** Staff Dashboard with HTMX polling/websockets.

<!-- end list -->

```
```