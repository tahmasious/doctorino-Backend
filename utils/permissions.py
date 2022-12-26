from rest_framework import permissions


class IsHotelOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.hotel_owner.user == request.user


class IsDoctorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class HasHotelOwnerRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_hotel_owner


class HasDoctorRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_doctor
