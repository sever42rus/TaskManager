from rest_framework.permissions import BasePermission


class UserRoomEdit(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return bool(obj.room_permission.filter(user=request.user, edit=True))


class UserColumnEdit(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return bool(obj.room.room_permission.filter(user=request.user, edit=True))
