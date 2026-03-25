from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)
    return wrapped_view


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            if "role" not in session:
                flash("Access denied.")
                return redirect(url_for("auth.login"))
            if session.get("role") != required_role:
                flash("You are not authorised to access this page.")
                return redirect(url_for("auth.login"))
            return view_func(*args, **kwargs)
        return wrapped_view
    return decorator