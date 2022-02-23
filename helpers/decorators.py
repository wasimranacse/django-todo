from django.contrib.auth.decorators import user_passes_test


def check_user_status(user):
    return not user.is_authenticated

user_logout_required = user_passes_test(check_user_status, '/', None)

# Logged in users won't be able to access login/register page
def auth_user_restricted_access(viewfunc):
    return user_logout_required(viewfunc)
