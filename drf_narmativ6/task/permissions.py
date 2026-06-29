from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    GET, HEAD, OPTIONS so'rovlariga hamma uchun ruxsat beradi.
    PUT, PATCH, DELETE faqat post (task) egasiga ruxsat beriladi.
    """
    def has_object_permission(self, request, view, obj):
    # Safe methods (GET, HEAD, OPTIONS) - xavfsiz so'rovlar
     if request.method in permissions.SAFE_METHODS:
        return True

    # O'zgartirish va o'chirish faqat ob'ekt egasiga (author yoki owner) ruxsat
    # Agar sening modelingda maydon nomi 'author' bo'lsa 'obj.author' qiling, 'owner' bo'lsa 'obj.owner'
     return obj.author == request.user