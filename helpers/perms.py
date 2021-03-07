def global_default_permission(user, obj, perm):
    if user.is_anonymous:
        return False
    return user.is_admin
