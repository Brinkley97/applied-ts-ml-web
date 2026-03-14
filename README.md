# Django Base Setup (Template)

🚨 **MASTER TEMPLATE - DO NOT DEPLOY DIRECTLY** 🚨

This repository serves as the foundational boilerplate for future Django projects. It includes a custom user model, pre-configured settings, and a standardized folder structure.

**When starting a new project, copy this folder first.**

---

## Phase 1: Environment Setup

These steps set up the Python environment using `uv`.

### 1. Prerequisites
Before you start, install Python, a code editor, and the uv tool. To install Python, go to https://www.python.org/downloads/ and download the latest Python 3.12+ version for your computer. Run the installer, and on Windows make sure you check the box that says “Add Python to PATH” before clicking Install. After installation, you can confirm it worked by opening a terminal and typing `python --version` (or `python3 --version` on some Macs). If Python isn’t found on macOS, you may need to install it using the official installer from the same Python website, then reopen your terminal.

Before you can “open your project folder” in VS Code, you first need to download the code from GitHub onto your computer. Start by going to https://github.com and creating a free account (Sign up, verify your email, and log in). Next, install GitHub Desktop: on Mac you can search “GitHub Desktop” online and download it from https://desktop.github.com (there isn’t usually an App Store version), and on Windows you can also download it from the same link. Open GitHub Desktop and sign in with your GitHub account. Then, open your web browser, go to the project’s repository page (the owner will send you a link), and click the green Code button, then choose Open with GitHub Desktop. GitHub Desktop will open and ask where to save the project on your computer—choose a location you can easily find (like Desktop or Documents), then click Clone. When it finishes downloading, open VS Code, click File → Open Folder…, and select the folder GitHub Desktop just created (it will contain a file named manage.py). Now you’ve opened the project correctly and can continue with the rest of the setup steps.



### 2. Initialization
Run these commands in your terminal to set up the virtual environment:

```bash
# Initialize uv (if not already done)
uv init

# Create the virtual environment
uv venv

# Activate the environment
source .venv/bin/activate
# Windows: .venv\Scripts\active

# Install Django and environment variables
uv pip install django
uv pip install django django-crispy-forms crispy-bootstrap5
uv pip compile pyproject.toml -o requirements.txt
```

## Phase 2 (Database & Admin Setup — do this once): 
First, build the database by running `python manage.py migrate`. 
Next, create an admin account by running `python manage.py createsuperuser`, then follow the prompts to enter a username (for example, admin), email, and password. Note: your password will not visibly appear while you type—this is normal.

## Phase 3 (Running the Website — do this every time): 
Whenever you want to work on the site or show it to someone, start the server `python manage.py runserver` and then open the site in your browser.

### 2. View the Site
Once the server is running, open your web browser and click these links:
| Page | URL | Description |
| :--- | :--- | :--- |
| **Home / Feed** | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) | The main landing page. |
| **Register** | [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/) | Create a new generic user account. |
| **Login** | [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/) | Log in to an existing account. |
| **Profile** | [http://127.0.0.1:8000/profile/](http://127.0.0.1:8000/profile/) | View your user details (must be logged in). |
| **Admin Panel** | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) | The "CEO" backend. Use the superuser account you created in Phase 2. |

## Phase 4: Test Features

1. [ ] Sign in
2. [ ] Sign out
3. [ ] User that is signed in can update their post and not anyone else's post
4. [ ] User that is signed in can delete their post and not anyone else's post
5. [ ] User that is signed in can update their profile and not anyone else's profile
6. [ ] Can access database as superuser
