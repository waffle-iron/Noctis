"""
utilities for noctis. Simple tools and extras.
"""
def getUsername(request):
    username = None
    if request.user.is_authenticated():
        return request.user.username
    else:
        raise "Username doesn't exist."
