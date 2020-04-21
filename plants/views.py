from rest_framework import viewsets
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import PlantSerializer


class PlantViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PlantSerializer

    def get_queryset(self):
        return self.request.user.plants.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
