from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    message = 'Should be AdminOrReadOnly'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin())
        )


class IsAdminOrSuperUser(BasePermission):
    message = 'Should be Admin or SU'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()


class UpdatingNotYourContentPermission(BasePermission):
    """Updating (deleting) not your content is forbidden."""
    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, object):
        if request.method not in SAFE_METHODS:
            if request.user.is_anonymous:
                return False
            return (request.user == object.author
                    or request.user.is_admin()
                    or request.user.is_moderator())
        return True
