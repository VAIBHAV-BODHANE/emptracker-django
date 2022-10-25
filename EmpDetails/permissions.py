from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):

    allowed_methods = ('PUT', 'PATCH')
    not_allowed_methods = ('POST')

    message = "You have no permission to create/delete the user!"

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method not in self.not_allowed_methods:
            return True
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if (request.method in self.allowed_methods) and (obj == request.user):
            return True
        if request.method in self.not_allowed_methods and (obj == request.user):
            return False
        return False
        

class EmpOrAdmin(BasePermission):

    not_allowed_methods = ('DELETE')

    message = "You cannot delete leave request"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser and request.method not in self.not_allowed_methods:
            return True
        if request.method not in self.not_allowed_methods and obj.user == request.user:
            return True