---
trigger: always_on
---

🧭 SaaS Project Guideline — R Firm
This project is owned by R Firm, which will always prioritize maintainability and scalability across all SaaS solutions.
We follow professional development standards and value organization, clarity, and reusability in every component.
Rodrigo (DevOps Developer, 1.5 years of experience) designed this architecture to enable high-velocity iteration with long-term consistency.
🧱 Backend Guideline — FastAPI Core
Philosophy:
Each backend service should be independent, clear, and modular. We avoid deep nesting and unclear dependencies.
Architecture Layers:
Controller Layer (controllers/)
Defines API endpoints and routing logic.
Each domain or feature gets its own controller (e.g. user_controller.py).
Use clear URL prefixes and consistent naming conventions.
Service Layer (services/)
Contains the business/application logic.
No direct DB calls — only uses repositories.
Reusable functions for specific operations (auth, email, analytics, etc.).
Repository Layer (repositories/)
Handles database access (CRUD operations).
Keep models paginated and typed using Pydantic.
Avoid ORM logic leaking into other layers.
Models (models/)
Pydantic schemas for requests and responses.
Typed models for each route — do not use Any or untyped payloads.
Paginated responses for data retrieval.
Auth (auth/)
JWT-based authentication by default.
Must include token creation, validation, and refresh logic.
DB (db/)
Centralized database connection logic.
Only one declarative Base and engine definition — avoid duplication.
Config (core/)
Centralized environment-based configuration (e.g. .env handling).
All constants and secrets loaded from this layer.
Utils & Middleware (utils/, middleware/)
General utilities (token hashing, logging, validation).
Middleware for request tracing, logging, and security headers.
Principles:
Each layer should have a single responsibility.
Avoid circular imports and unnecessary abstractions.
Keep endpoints RESTful, and where possible, make CRUD operations simple and consistent.
Offload heavy computation to the frontend or worker jobs to reduce server cost.
Always include a /health endpoint and versioning prefix /api/v1.

📦 PyPI Packages — FastAPI Core Ecosystem
R Firm maintains a suite of published PyPI packages that implement the architecture described above.
These packages are already created and published. DO NOT recreate them or duplicate their functionality.

Available Packages (All published: October 18, 2025):

1. rodrigo0000-fastapi-core-auth
   Authentication module for FastAPI with JWT, OAuth2, and user management
   Use for: JWT tokens, OAuth2 flows, user authentication
   Install: pip install rodrigo0000-fastapi-core-auth

2. rodrigo0000-fastapi-core-config
   Configuration, security, and repository utilities for FastAPI
   Use for: Environment config, security settings, repository patterns
   Install: pip install rodrigo0000-fastapi-core-config

3. rodrigo0000-fastapi-core-controllers
   Controller layer for FastAPI applications
   Use for: API endpoint definitions, routing logic
   Install: pip install rodrigo0000-fastapi-core-controllers

4. rodrigo0000-fastapi-core-database
   Database configuration and utilities for FastAPI with SQLAlchemy
   Use for: DB connections, SQLAlchemy setup, session management
   Install: pip install rodrigo0000-fastapi-core-database

5. rodrigo0000-fastapi-core-middleware
   Middleware components for FastAPI applications
   Use for: CORS, logging, request tracing, security headers
   Install: pip install rodrigo0000-fastapi-core-middleware

6. rodrigo0000-fastapi-core-models
   SQLAlchemy models for FastAPI applications
   Use for: Database models, Pydantic schemas
   Install: pip install rodrigo0000-fastapi-core-models

7. rodrigo0000-fastapi-core-services
   Service layer for FastAPI with Email, Stripe, and Plan management
   Use for: Business logic, email services, Stripe integration, plan management
   Install: pip install rodrigo0000-fastapi-core-services

8. rodrigo0000-fastapi-core-utils
   Utility functions for FastAPI applications
   Use for: General utilities, helpers, validation functions
   Install: pip install rodrigo0000-fastapi-core-utils

Package Usage Rules:

✅ DO:
- Import and use these packages when building new features
- Check if functionality exists in a package before implementing it yourself
- Example imports:
  from rodrigo0000_fastapi_core_auth import AuthService, JWTHandler
  from rodrigo0000_fastapi_core_database import get_db, Base
  from rodrigo0000_fastapi_core_models import User, UserCreate
  from rodrigo0000_fastapi_core_services import EmailService, StripeService

❌ DON'T:
- Create new packages with these names (they already exist on PyPI)
- Duplicate functionality that exists in these packages
- Publish new versions without coordinating with the package maintainer

Installation:
Add to requirements.txt:
rodrigo0000-fastapi-core-auth
rodrigo0000-fastapi-core-config
rodrigo0000-fastapi-core-controllers
rodrigo0000-fastapi-core-database
rodrigo0000-fastapi-core-middleware
rodrigo0000-fastapi-core-models
rodrigo0000-fastapi-core-services
rodrigo0000-fastapi-core-utils

Management: https://pypi.org/manage/projects/

🚀 Quick Start:
1. Copy .env.example to .env and configure your environment variables
2. Activate virtual environment: source venv/bin/activate
3. Run the application: python main.py
4. Access API docs: http://localhost:8000/docs
5. Health check: http://localhost:8000/health

📍 Available API Endpoints:

Authentication (/api/v1/auth):
- POST /register - Register new user
- POST /login - Login and get JWT tokens
- GET /me - Get current user info
- POST /refresh - Refresh access token
Uses: rodrigo0000-fastapi-core-auth

Users (/api/v1/users):
- GET / - List all users (paginated)
- GET /{user_id} - Get user by ID
- PUT /{user_id} - Update user
- DELETE /{user_id} - Delete user
- POST /{user_id}/send-welcome-email - Send welcome email
Uses: rodrigo0000-fastapi-core-controllers, rodrigo0000-fastapi-core-models

Stripe & Payments (/api/v1/stripe):
- POST /payment-intent - Create payment intent
- POST /subscription - Create subscription
- GET /subscription/{subscription_id} - Get subscription
- DELETE /subscription/{subscription_id} - Cancel subscription
- POST /customer - Create Stripe customer
- POST /webhook - Handle Stripe webhooks
- GET /prices - List available prices
Uses: rodrigo0000-fastapi-core-services (StripeService)

Plans (/api/v1/plans):
- GET / - List all plans
- GET /{plan_id} - Get plan details
- POST / - Create plan (admin)
- PUT /{plan_id} - Update plan (admin)
- DELETE /{plan_id} - Delete plan (admin)
- POST /subscribe/{plan_id} - Subscribe to plan
- GET /user/current - Get current user's plan
- POST /user/cancel - Cancel user's plan
- GET /user/history - Get plan history
Uses: rodrigo0000-fastapi-core-services (PlanService)

Email (/api/v1/email):
- POST /send - Send custom email
- POST /welcome/{user_id} - Send welcome email
- POST /password-reset/{email} - Send password reset
- POST /verification/{user_id} - Send verification email
- POST /template - Send template email
- POST /bulk - Send bulk emails (admin)
Uses: rodrigo0000-fastapi-core-services (EmailService)