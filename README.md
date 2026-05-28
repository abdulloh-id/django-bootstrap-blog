# Django Bootstrap Blog

A production-ready, fully localized Django blog styled with Bootstrap. Built to easily switch between a personal portfolio blog and a multi-author platform with a single environment variable.

---

## Features

### Dual-Mode Architecture (`PERSONAL_BLOG_MODE`)

- **`PERSONAL_BLOG_MODE=True`** — Disables public registration and presents the site as a personal blog or portfolio
- **`PERSONAL_BLOG_MODE=False`** — Opens user registration and allows multiple authors to write and manage their own articles

### Multi-Language Support (i18n)

- Full site translation across **English**, **Uzbek**, and **Russian**
- Clean `.po` file structure organized by section for easy maintenance
- Compatible with `makemessages` and `compilemessages` Django management commands

### Custom Auth & Profile System

- Custom user model (`CustomUser`) via `get_user_model()` — safe and future-proof
- Automatic `Profile` creation on user signup via Django signals
- Separate forms for user info and profile avatar, processed in a single POST

### Content Features

- Rich-text article editor powered by **TinyMCE**
- Form rendering via **Django Crispy Forms**
- Article categories, tags, search, and pagination
- Comment system via `django_comments`
- Privacy Policy and Terms & Conditions pages

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.1.x |
| Runtime | Python 3.12+ |
| Frontend | Bootstrap 4, Themify Icons |
| Forms | Django Crispy Forms |
| Static Files | WhiteNoise |
| Database | MySQL |
| Editor | TinyMCE |

---

## Project Structure

```
├── config/          # Project settings and URLs
├── accounts/        # Custom user model, auth views and forms
├── articles/        # Articles, categories, tags, comments
├── pages/           # About, Contact, Privacy Policy, Terms
├── locale/          # Translation files (en, uz, ru)
├── templates/       # HTML templates
├── static/          # CSS, JS, images
└── manage.py
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/django-bootstrap-blog.git
cd django-bootstrap-blog
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Key variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key
PERSONAL_BLOG_MODE=False
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

See `.env.example` for the full list.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Compile translations

```bash
python manage.py compilemessages
```

### 7. Start the server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

---

## Localization Workflow

To add or update translated strings:

```bash
# Extract new strings from templates and views
python manage.py makemessages -l uz -l ru

# Edit locale/uz/LC_MESSAGES/django.po and locale/ru/LC_MESSAGES/django.po
```

Then compile using one of two options:

**Option A — Standard Django:**
```bash
python manage.py compilemessages
```
Requires GNU gettext binaries installed on your system. Works out of the box on Linux/macOS. On Windows, you may need to install gettext manually.

**Option B — Custom script (recommended for Windows):**
```bash
python scripts/compile_po.py
```
A pure Python alternative using `polib` — no external binaries needed. Also automatically removes duplicate translation entries before compiling, which prevents gettext crashes from messy `.po` files.

Install the dependency if you haven't already:
```bash
pip install polib
```

---

## License

Distributed under the MIT License. See `LICENSE` for details.
