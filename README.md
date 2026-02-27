# Recipe Management API

Backend REST API built with Django and Django REST Framework for managing recipes, categories, and ingredients.

## Tech Stack
- Django
- Django REST Framework
- DRF Token Authentication
- SQLite (development)

## Setup
1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Apply migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`

## Authentication
- Type: `TokenAuthentication`
- Header format: `Authorization: Token <token>`

## API Root
- `GET /`
- Returns links for:
  - register
  - login
  - admin_login
  - categories
  - ingredients
  - recipes

## Endpoints

### Auth
- `POST /api/auth/register/` (public)
- `POST /api/auth/login/` (public)
- `POST /api/auth/logout/` (authenticated)
- `GET /api/users/me/` (authenticated)

### Categories
- `GET /api/categories/` (public)
- `GET /api/categories/{id}/` (public)
- `POST /api/categories/` (admin only)
- `PUT /api/categories/{id}/` (admin only)
- `PATCH /api/categories/{id}/` (admin only)
- `DELETE /api/categories/{id}/` (admin only)

### Ingredients
- `GET /api/ingredients/` (public)
- `GET /api/ingredients/{id}/` (public)
- `POST /api/ingredients/` (admin only)
- `PUT /api/ingredients/{id}/` (admin only)
- `PATCH /api/ingredients/{id}/` (admin only)
- `DELETE /api/ingredients/{id}/` (admin only)

### Recipes
- `GET /api/recipes/` (public)
- `GET /api/recipes/{id}/` (public)
- `POST /api/recipes/` (admin only)
- `PUT /api/recipes/{id}/` (admin only)
- `PATCH /api/recipes/{id}/` (admin only)
- `DELETE /api/recipes/{id}/` (admin only)

### Recipe Filters/Search
- `GET /api/recipes/category/{category_id}/` (public)
- `GET /api/recipes/ingredient/{ingredient_id}/` (public)
- `GET /api/recipes/search/?title=<query>` (public)

## Recipe Payload Requirements
For create/update recipe requests, these fields are required:
- `title`
- `description`
- `instructions`
- `category` (category ID)
- `ingredients` (non-empty list of ingredient IDs)

Example:
```json
{
  "title": "Omelet",
  "description": "Quick breakfast",
  "instructions": "Beat eggs and cook",
  "category": 1,
  "ingredients": [1, 2]
}
```

## Admin Access
- Django admin login page: `/admin/login/`
- Create admin from terminal:
  - `python manage.py createsuperuser`
