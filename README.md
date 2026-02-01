# Multi-Tenant SaaS Backend (Django + DRF)  -->  UNDER-DEVELOPMENT

A production-oriented **multi-tenant SaaS backend** inspired by Amazon/Fiverr-style platforms. The system supports **multiple organizations per user**, strict **tenant isolation**, **role-based access control**, and **secure ownership transfer**.

This project focuses on **correct domain modeling, security, and data integrity** rather than premature optimization.

---

## 🚀 Features Implemented So Far

### 1. Authentication & Users

* Custom `User` model (email-based login)
* JWT authentication
* Email verification support
* Permissions via DRF

### 2. Organizations (Tenants)

* Users can belong to **multiple organizations**
* Organization creation and membership management
* Strict tenant boundary enforced at API level

### 3. Organization Membership & Roles

* `OrganizationMember` as the join model
* Roles:

  * `OWNER` (exactly one per organization)
  * `ADMIN`
  * `MEMBER`
* **Database-level constraint** enforcing single owner per organization

### 4. Ownership Transfer (Critical Domain Operation)

* Secure ownership transfer endpoint
* Only current owner can transfer ownership
* New owner must:

  * Exist
  * Have verified email
  * Already be a member of the organization
* Uses **transactional integrity** (`transaction.atomic`)
* Role swap (OWNER → ADMIN, MEMBER/ADMIN → OWNER)

---

## 🧠 Key Design Decisions

### Multi-Tenancy Strategy

* **Shared database, tenant-scoped rows**
* Every tenant-owned model references `Organization`
* Organization context passed explicitly via URL (`/organizations/{org_id}/...`)

### Why `OrganizationMember`?

* Represents the relationship, not just membership
* Avoids implicit many-to-many magic
* Allows role changes without deleting history

### Why Database Constraints?

* Business rule: **exactly one OWNER per organization**
* Enforced at DB level to prevent race conditions

---

## 📁 Project Structure (Current)

```text
backend/
├── accounts/
│   ├── models.py        # Custom User model
│   ├── managers.py     # UserManager
│   ├── permissions.py  # Custom permissions (e.g. VerifiedEmailPermission)
│   └── auth/            # JWT configuration
│
├── organizations/
│   ├── models.py        # Organization, OrganizationMember
│   ├── views.py         # Ownership transfer & org-related APIs
│   ├── permissions.py  # Org-level permission checks
│   └── urls.py
│
├── core/
│   ├── middleware.py    # (Optional) tenant resolution middleware
│   └── utils.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
│
├── requirements.txt
└── manage.py
```

---

## 🔐 Security & Integrity Guarantees

* No cross-organization data access
* All privileged operations verify:

  * Authenticated user
  * Organization membership
  * Role permissions
* Ownership transfer is **atomic and race-condition safe**

---

## 🧪 What’s Next (Planned)

* Organization invitations (email-based)
* Service layer for domain operations
* Tenant-scoped permissions (DRF Permission Classes)
* Customer Management (CRM domain)
* Product & Order management
* Audit logs for sensitive actions
* Test coverage for multi-tenant invariants

---

## 🛠 Tech Stack

* **Backend**: Django, Django REST Framework
* **Auth**: JWT (SimpleJWT)
* **Database**: PostgreSQL (recommended)
* **Deployment**: Gunicorn, Whitenoise

---

## ⚠️ Important Notes

* This project prioritizes **correctness over premature optimization**
* Critical paths (ownership, permissions) are intentionally explicit
* DB calls are minimized where necessary, not where dangerous

---

## 📜 License

MIT (or update as needed)

---

## 👤 Author

Built as a learning-focused, production-grade SaaS backend with emphasis on:

* Multi-tenancy
* Domain modeling
* Security
* Data integrity

Contributions and reviews are welcome.
