from api.auth.auth import create_auth_bp
from api.auth.users import create_users_bp

users_bp = create_users_bp()

auth_bp = create_auth_bp()
