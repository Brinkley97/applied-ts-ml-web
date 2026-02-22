# Django Base Setup (Template)

🚨 **MASTER TEMPLATE - DO NOT DEPLOY DIRECTLY** 🚨

This repository serves as the foundational boilerplate for future Django projects. It includes a custom user model, pre-configured settings, and a standardized folder structure.

**When starting a new project (e.g., Rapha, SchoolApp), copy this folder first.**

---

## Phase 1: Environment Setup

These steps set up the Python environment using `uv`.

### 1. Prerequisites
- Python 3.12+ installed
- `uv` installed (`pip install uv`)
- Git installed

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
uv pip compile pyproject.toml -o requirements.txt

