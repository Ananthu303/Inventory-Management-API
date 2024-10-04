import logging

from django.core.cache import cache
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item
from .serializers import ItemSerializer, RegisterSerializer

logger = logging.getLogger("api_requests")


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"Registration successful for : {user.username}")
            return Response(
                {
                    "success": f"Registration successful ! Hello {user.username}",
                },
                status=status.HTTP_201_CREATED,
            )
        logger.error(f"Registration failed !")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        items = self.queryset 
        if not items.exists():
            logger.error("No items Found.")
            return Response({"error": "No items found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            item_name = serializer.validated_data["name"]
            if Item.objects.filter(name=item_name).exists():
                logger.error(
                    f"Item creation failed: Item with name '{item_name}' already exists."
                )
                return Response(
                    {"error": "Item already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.perform_create(serializer)
            logger.info("Item created successfully: %s", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Item creation failed: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        item_id = kwargs.get("pk")
        item_cache_key = f"item_{item_id}"
        cached_item = cache.get(item_cache_key)

        if cached_item:
            logger.info(f"Item with ID {item_id} retrieved from cache.")
            return Response(cached_item)

        try:
            item = self.get_object()
            item_data = self.get_serializer(item).data
            cache.set(item_cache_key, item_data)
            logger.info(f"Item with ID {item_id} retrieved from database and cached.")
            return Response(item_data)
        except Http404:
            logger.error(f"Item with ID {item_id} not found.")
            return Response(
                {"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, *args, **kwargs):
        try:
            item_id = kwargs.get("pk")
            item = self.get_object()
        except Http404:
            return Response(
                {"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        item_cache_key = f"item_{item_id}"
        cache.delete(item_cache_key)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            item_id = kwargs.get("pk")
            item = self.get_object()
            item.delete()
            item_cache_key = f"item_{item_id}"
            cache.delete(item_cache_key)
            logger.info(f"Item with ID {item_id} deleted successfully.")

            return Response(
                {"message": "Item deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Http404:
            logger.error("Deletion failed: Item not found.")
            return Response(
                {"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND
            )
