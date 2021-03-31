from rest_framework.permissions import IsAuthenticated, AllowAny


class AccessUserViews:
    permission_classes = [IsAuthenticated, ]
