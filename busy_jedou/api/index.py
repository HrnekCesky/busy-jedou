from busy_jedou import app

# Vercel's Python runtime expects a file named index.py under /api.
# It should export a WSGI application called `app` or a function named `handler`.
# We expose the existing Flask app as `app` so Vercel can use it.

# The busy_jedou package already creates `app` in busy_jedou/__init__.py

# Expose it here:
from busy_jedou import app as application

# Some Vercel runtimes expect `app` or `application`, keep both refs.
app = application
