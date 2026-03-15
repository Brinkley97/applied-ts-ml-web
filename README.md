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
# Windows: .venv\Scripts\activate

# Install Django and environment variables
uv pip install django django-crispy-forms crispy-bootstrap5
uv pip compile pyproject.toml -o requirements.txt
```

## Phase 2 (Database & Admin Setup — do this once): 

First, build the database by running `python manage.py migrate`. 
Next, create an admin account by running `python manage.py createsuperuser`, then follow the prompts to enter a username (for example, admin), email, and password. Note: your password will not visibly appear while you type—this is normal.

## Phase 3 (Running the Website — do this every time): 

Whenever you want to work on the site or show it to someone, start the server `python manage.py runserver` and then open the site in your browser.

### 1. View the Site
Once the server is running, open your web browser and click these links:
| Page | URL | Description |
| :--- | :--- | :--- |
| **Home / Feed** | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) | The main landing page. |
| **Register** | [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/) | Create a new generic user account. |
| **Login** | [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/) | Log in to an existing account. |
| **Profile** | [http://127.0.0.1:8000/profile/](http://127.0.0.1:8000/profile/) | View your user details (must be logged in). |
| **Admin Panel** | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) | The "CEO" backend. Use the superuser account you created in Phase 2. |

## Phase 4: Test Features

- [ ] Sign in
- [ ] Sign out
- [ ] User that is signed in can update their post and not anyone else's post
- [ ] User that is signed in can delete their post and not anyone else's post
- [ ] User that is signed in can update their profile and not anyone else's profile
- [ ] Can access database as superuser

## Phase 5: Git Workflow (Base Repo + Startups)

### `django-base-setup` (The Base Repository)

- **`main`**
  - Canonical shared base (tutorial + your universal additions)
  - This is the branch that all startup projects should sync from
- **`tutorial`**
  - Tutorial-only snapshot/reference branch
  - Only update this branch when you are strictly following the tutorial
- **`dev`**
  - Where you build and test new base features first
  - When a base feature is stable, merge **`dev → main`**
- **Feature branches (optional)**
  - Create a branch off `dev` for a specific change (example: `feature/navbar`)
  - Merge **`feature → dev → main`**

### Creating a New Startup Repo from the Base (same GitHub account)

- **Important:** Create the new GitHub repository first and **do NOT** initialize it with a README, `.gitignore`, or license.

#### Template Commands
```bash
# 1) Clone the base repo into a NEW local folder name
git clone https://github.com/<your-username>/django-base-setup.git <new-project-folder>
cd <new-project-folder>

# 2) Point this local repo at the NEW GitHub repo you created
git remote set-url origin https://github.com/<your-username>/<new-repo-name>.git

# 3) Push the code to the new repo
git push -u origin main

# 4) Push tags and all branches (important if you have dev/tutorial branches)
git push --tags
git push --all
```

#### Example
```bash
git clone https://github.com/Brinkley97/django-base-setup.git applied-ts-ml-web
cd applied-ts-ml-web
git remote set-url origin https://github.com/Brinkley97/applied-ts-ml-web.git
git push -u origin main
git push --tags
git push --all
```
- **Important:** Rename the local folder (or clone directly into the new name) so you don’t end up with a folder called `django-base-setup` for every startup.

### Pushing Base Updates (`django-base-setup`) and Pulling Them Into a Startup Repo

#### A) Push your changes to the **base repo** (`django-base-setup/dev`)

##### Terminal (Recommended)
```bash
cd path/to/django-base-setup
git checkout dev
git add .
git commit -m "Update README"
git push -u origin dev
```

##### GitHub Desktop (No Terminal)
```bash
# 1) Open GitHub Desktop
# 2) Select the repository: django-base-setup
# 3) Switch to the dev branch:
#    - Click "Current Branch" and select "dev"
#    - If dev doesn't exist: click "New Branch", name it "dev", create it
# 4) Make edits in VS Code and save files
# 5) Back in GitHub Desktop:
#    - Enter a commit message (example: "Update README")
#    - Click "Commit to dev"
# 6) Click "Push origin" to push django-base-setup/dev to GitHub
```

---

#### B) Pull base changes into the **startup repo** (`startup/dev`) and push

##### Terminal (Recommended)
```bash
cd path/to/<startup-repo>

Important: git remote add upstream ... is a one-time setup. If you see an error like *remote upstream already exists**, skip this step and continue.
# (one-time setup) add the base repo as "upstream"
git remote add upstream https://github.com/Brinkley97/django-base-setup.git

# fetch the latest updates from the base repo
git fetch upstream

# merge base changes into your startup dev branch
git checkout dev
git merge upstream/main
# or, if you specifically want the base dev branch:
# git merge upstream/dev

# push the updated startup dev branch
git push -u origin dev
```

##### GitHub Desktop (No Terminal)
```bash
# Note: GitHub Desktop does NOT have a clean "add upstream remote + merge upstream branch"
# workflow built into the UI. The simplest approach is:
#
# 1) Use Terminal just for the upstream merge step (above), OR
# 2) Open the startup repo on GitHub.com and manually apply changes (not recommended).
#
# Recommended: do the upstream merge in Terminal, then use GitHub Desktop to commit/push.
#
# After running the terminal merge:
# 1) Open GitHub Desktop
# 2) Select the startup repo (e.g., applied-ts-ml-web)
# 3) Ensure you are on the dev branch
# 4) You should see the merged changes listed
# 5) Click "Push origin" (if not already pushed)
```

### `startup[i]` (Each Startup Repository)

- **Initial setup**
  - Fork (or create a new repo based on) `django-base-setup/main`

- **Internal workflow**
  - Use a normal `main` + `dev` workflow inside the startup repo
  - Do active work in `startup[i]/dev`
  - Merge completed work **`startup[i]/dev → startup[i]/main`**

- **Feature branches (recommended)**
  - Create a branch for each task (example: `startup[i]/feature/signup-ui`)
  - Merge **`startup[i]/feature → startup[i]/dev → startup[i]/main`**

- **Receiving updates from the base repo**
  - Periodically merge updates from **`django-base-setup/main`** into **`startup[i]/dev`**
  - Test the startup after pulling base updates
  - Then merge **`startup[i]/dev → startup[i]/main`**
